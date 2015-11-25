#!/usr/bin/env bash

read -r -d '' HELP <<-'EOF'

Automate pulling and then prepping documents from Managed Masters.
Documents must be Penn in Hand.  Processes all `todo` and `retrieved`
files found in OPENN_TODO_DIR.

Requires an `opennrc` file.  By default script looks in /etc/opennrc.
Alternately you can set the OPENN_RC environment or use the `-c`
option to specify an alternate path, like $HOME/.opennrc.

EOF

cmd=`basename $0`
export COMMAND=$cmd
export HELP
source `dirname $0`/../bin/op-functions
export LOG_LEVEL=$LEVEL_DEBUG

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
      version
      mm_help
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
OPGET_PID_FILE=$OPENN_RUN_DIR/op-get.pid
OPPREP_PID_FILE=$OPENN_RUN_DIR/op-prep.pid

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
  rm -f $tmp.?
  rm -f $OPMM_PID_FILE
}

change_status() {
    cs_currfile=$1
    cs_newstatus=$2
    cs_base=`echo $cs_currfile | sed 's/\.[-a-zA-Z_]*$//'`
    cs_newfile=$cs_base.$cs_newstatus
    mv -v $cs_currfile $cs_newfile 1>&2
    if [[ $? -ne 0 ]]
    then
        echo "NOSUCHFILE"
        return 1
    else
        echo $cs_newfile
        return 0
    fi
}

get_field() {
    # path to the todo file
    gf_todo=$1
    # the field name
    gf_field=$2
    if [[ -f $gf_todo ]]
    then
        if grep -i $gf_field $gf_todo >/dev/null 2>&1
        then
            grep $gf_field $gf_todo | awk -F ':' '{ print $2 }' | sed -e 's/^ *//' -e 's/ *$//'
            return $?
        else
            error_no_exit "Cannot find field '$gf_field' in todo file '$gf_todo'" >&2
            return 1
        fi
    else
        error_no_exit "Cannot find todo file '$gf_todo'" >&2
        return 1
    fi
    return 0
}

# quit_op_mm_nicely() {
#   # use 10 (SIGUSR1) if no argument
#   qomn_sig=${1:-10}
#   message "Received kill -${qomn_sig}"
#   if [[ -f $OP ]]
#   then
#   fi

#   if [ -f $MM_CTRL_PID ]; then
#     the_pid=`cat $MM_CTRL_PID`
#     kill -${qomn_sig} $the_pid
#     message "Sent kill -${qomn_sig} to controller $the_pid"
#     while [ -e /proc/$the_pid ]; do sleep 0.1; done
#     message "Controller $the_pid has stopped"
#   else
#     warning "No MM_CTRL_PID found: $MM_CTRL_PID"
#   fi
#   sleep 2
# }

if ls $OPENN_TODO_DIR/*.todo >/dev/null 2>&1; then
    for todo in $OPENN_TODO_DIR/*.todo; do
        # clear the vars
        path=; prep=; bibid=; base=
        path=`get_field $todo source`
        if [[ $? -ne 0 ]]; then continue; fi
        bibid=`get_field $todo bibid`
        if [[ $? -ne 0 ]]; then continue; fi
        todo=`change_status $todo getting`
        op-get -b $bibid $path $OPENN_PACKAGE_DIR/Prep
        status=$?
        if [[ $status -ne 0 ]]; then
            error_no_exit "Could not get $path with BibID $bibid"
            error_no_exit "Marking $todo failed"
            change_status $todo GET_FAILED
        else
            message "Retrieved $path"
            todo=`change_status $todo retrieved`
            base=`basename $path`
            echo "prepsource: ${OPENN_PACKAGE_DIR}/Prep/${base}" >> $todo
        fi
    done
else
    warning "No *.todo files found in $OPENN_TODO_DIR"
fi

if ls $OPENN_TODO_DIR/*.retrieved >/dev/null 2>&1
then
    for todo in $OPENN_TODO_DIR/*.retrieved
    do
        message "Looking at todo file: $todo"
        # clear the vars
        path=; prep=; base=; prepsource=
        prep=`get_field $todo coll_prep`
        if [[ $? -ne 0 ]]; then continue; fi
        message "Found coll_prep: $coll_prep"
        prepsource=`get_field $todo prepsource`
        if [[ $? -ne 0 ]]; then continue; fi
        message "Found prepsource: $prepsource"
        base=`basename $prepsource`

        todo=`change_status $todo prepping`
        op-prep $prep $prepsource
        if [[ $? -ne 0 ]]
        then
            change_status $todo PREP_FAILED
            error_no_exit "Unable to prep $source"
        else
            change_status $todo PREP_SUCCEEDED
        fi
    done
else
    warning "No *.retrieved files found in $OPENN_TODO_DIR/"
fi

# trap "quit_op_mm_nicely 10; cleanup; exit" 10
trap "cleanup; exit 1" 1 2 3 13 15
trap "cleanup; exit" 0




### EXIT
# http://stackoverflow.com/questions/430078/shell-script-templates
cleanup
trap 0
exit 0
