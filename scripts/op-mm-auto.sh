#!/usr/bin/env bash

read -r -d '' HELP <<-'EOF'

Automate pulling and then prepping documents from Managed Masters.
Documents must be Penn in Hand.  Processes all `todo` and `retrieved`
files found in OPENN_TODO_DIR.

Requires an `opennrc` file.  By default script looks in /etc/opennrc.
Alternately you can set the OPENN_RC environment or use the `-c`
option to specify an alternate path, like $HOME/.opennrc.

EOF

echo $$

cmd=`basename $0`

export COMMAND=$cmd
export HELP
source `dirname $0`/../bin/op-functions
source `dirname $0`/op-mm-functions
export LOG_LEVEL=$LEVEL_DEBUG
scripts_dir=`dirname $0`
scripts_dir=`realpath $scripts_dir`

usage() {
    cat <<EOF
Usage: $cmd [-c /path/to/opennrc]

Option
======

    -c /path/to/opennrc
        Specify the path to an opennrc file [default: /etc/opennrc].
EOF
}

### OPTIONS
while getopts "hc:" opt; do
  case $opt in
    h)
      usage
      exit 1
      ;;
    c)
      OPENN_RC=$OPTARG
      ;;
    \?)
      echo "ERROR Invalid option: -$OPTARG" >&2
      echo ""
      usage
      exit 1
      ;;
  esac
done

shift $((OPTIND-1))

if [[ -f ${OPENN_RC:=/etc/opennrc} ]]
then
    source $OPENN_RC
else
    error_no_exit "Could not find required file '$OPENN_RC'" >&2
    error "Please create $OPENN_RC or use an alternate set to var OPENN_RC" >&2
fi

OPMM_PID_FILE=$OPENN_RUN_DIR/${cmd}.pid
export OPMM_GET_PID_FILE=$OPENN_RUN_DIR/op-mm-get.pid
export OPMM_PREP_PID_FILE=$OPENN_RUN_DIR/op-mm-prep.pid

# PIDS
if [[ -n "$OPENN_RUN_DIR" ]] && [[ -d "$OPENN_RUN_DIR" ]] && [[ -w $OPENN_RUN_DIR ]];
then
    message "Using OPENN_RUN_DIR: '$OPENN_RUN_DIR'"
else
    error "OPENN_RUN_DIR doesn't exist or is not writable: '$OPENN_RUN_DIR'"
fi

if [[ -f $OPMM_PID_FILE ]]
then
  pid=`cat $OPMM_PID_FILE`
  error_no_exit "PID file exists: ${OPENN_OPMM_PID_FILE} with PID `cat $pid`" >&2
  ps x -o  "%p %r %y %x %c %a " | grep "$pid"
  exit 1
else
  echo $$ > $OPMM_PID_FILE
fi

### TEMPFILES
# From:
#   http://stackoverflow.com/questions/430078/shell-script-templates
# create a default tmp file name
tmp=${TMPDIR:-/tmp}/prog.$$

cleanup() {
    message "Cleaning up"
    rm -f $tmp.?
    for pidfile in $OPMM_PID_FILE $OPMM_PREP_PID_FILE $OPMM_GET_PID_FILE
    do
        if [[ -f $pidfile ]]
        then
            debug "Deleting PID file: $pidfile"
            rm -f $pidfile
        fi
    done
}

quit_op_mm_nicely() {
    # use 10 (SIGUSR1) if no argument
    qomn_sig=${1:-10}
    message "Received kill -${qomn_sig}"
    if [[ -f $OPMM_GET_PID_FILE ]]
    then
        cpid=`cat $OPMM_GET_PID_FILE`
        wait $cpid
        message "op-mm-get process stopped"
    fi
    cpid=
    if [[ -f $OPMM_PREP_PID_FILE ]]
    then
        cpid=`cat $OPMM_PREP_PID_FILE`
        wait $cpid
        qomn_exit=$?
        message "op-mm-prep process stopped"
    fi
    sleep 2
}

trap "quit_op_mm_nicely 10; cleanup; exit" 10
trap "cleanup; exit 1" 1 2 3 13 15
trap "cleanup; exit" 0

if ls $OPENN_TODO_DIR/*.todo >/dev/null 2>&1
then
    total=0
    count=0
    total=`ls $OPENN_TODO_DIR/*.todo | wc -l`
    for todo in $OPENN_TODO_DIR/*.todo
    do
        count=$(( count + 1 ))
        curr=`printf "%3d/%d" $count $total`
        message "TODO ${curr}; processing: $todo"
        $scripts_dir/op-mm-get.sh -c $OPENN_RC $todo
        if [[ $? -ne 0 ]]
        then
            error_no_exit "Get FAILED for: $todo"
        else
            message "Get SUCCEEDED for: $todo"
        fi
    done
else
    warning "No *.todo files found in $OPENN_TODO_DIR"
fi

if ls $OPENN_TODO_DIR/*.retrieved >/dev/null 2>&1
then
    total=0
    count=0
    total=`ls $OPENN_TODO_DIR/*.retrieved | wc -l`
    for todo in $OPENN_TODO_DIR/*.retrieved
    do
        count=$(( count + 1 ))
        curr=`printf "%3d/%d" $count $total`
        message "TODO ${curr}; processing: $todo"
        $scripts_dir/op-mm-prep.sh -c $OPENN_RC $todo
        if [[ $? -ne 0 ]]
        then
            error_no_exit "Prep FAILED for: $todo"
        else
            message "Prep SUCCEEDED for: $todo"
        fi
    done
else
    warning "No *.retrieved files found in $OPENN_TODO_DIR/"
fi

### EXIT
# http://stackoverflow.com/questions/430078/shell-script-templates
cleanup
trap 0
exit 0
