#!/usr/bin/env bash

read -r -d '' HELP <<-'EOF'

Peform op-get based on TODO_FILE
EOF

cmd=`basename $0`
export COMMAND=$cmd
export HELP
source `dirname $0`/../bin/op-functions
source `dirname $0`/op-mm-functions

usage() {
    cat <<EOF
Usage: $cmd [-c /path/to/opennrc] TODO_FILE

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

todo=$1
if [[ -n "$todo" ]] && [[ -f $todo ]]
then
    message "Using TODO_FILE: '$todo'"
else
    error "Cannot find TODO_FILE:: '$todo'"
fi

if [[ -f ${OPENN_RC:=/etc/opennrc} ]]
then
    source $OPENN_RC
else
    error_no_exit "Could not find required file '$OPENN_RC'" >&2
    error "Please create $OPENN_RC or use an alternate set to var OPENN_RC" >&2
fi

if [[ -n "$OPMM_GET_PID_FILE" ]]
then
    message "OPMM_GET_PID_FILE defined: $OPMM_GET_PID_FILE"
    # PIDS
    if [[ -n "$OPENN_RUN_DIR" ]] && [[ -d "$OPENN_RUN_DIR" ]] && [[ -w $OPENN_RUN_DIR ]];
    then
        message "Using OPENN_RUN_DIR: '$OPENN_RUN_DIR'"
    else
        error "OPENN_RUN_DIR doesn't exist or is not writable: '$OPENN_RUN_DIR'"
    fi

    if [[ -f $OPMM_GET_PID_FILE ]]
    then
        pid=`cat $OPMM_GET_PID_FILE`
        error_no_exit "PID file exists: ${OPENN_OPMM_GET_PID_FILE} with PID `cat $pid`" >&2
        ps x -o  "%p %r %y %x %c %a " | grep "$pid"
        exit 1
    else
        echo $$ > $OPMM_GET_PID_FILE
    fi
else
    warning "OPMM_GET_PID_FILE not defined; no PID file set"
fi

### TEMPFILES
# From:
#   http://stackoverflow.com/questions/430078/shell-script-templates
# create a default tmp file name
tmp=${TMPDIR:-/tmp}/prog.$$

cleanup() {
  rm -f $tmp.?
  if [[ -n "$OPMM_GET_PID_FILE" ]]
  then
      debug "Deleting OPMM_GET_PID_FILE: $OPMM_GET_PID_FILE"
      rm -f $OPMM_GET_PID_FILE
  fi
}

trap "cleanup; exit 1" 1 2 3 10 13 15
trap "cleanup; exit" 0

# clear the vars
path=; prep=; bibid=; base=
path=`get_field $todo source`
if [[ $? -ne 0 ]]
then
    error "Cannot retrieve field 'source' from $todo"
fi

bibid=`get_field $todo bibid`
if [[ $? -ne 0 ]]
then
    error "Cannot retrieve field 'bibid' from $todo"
fi

openn_prep_dir=$OPENN_PACKAGE_DIR/Prep
todo=`change_status $todo getting`
`dirname $0`/../bin/op-get -b $bibid $path $openn_prep_dir
status=$?
if [[ $status -ne 0 ]]; then
    change_status $todo GET_FAILED
    fail "op-get -b $bibid $path"
else
    message "Retrieved $path"
    todo=`change_status $todo retrieved`
    base=`basename $path`
    prepsource=${openn_prep_dir}/${base}
    echo "prepsource: ${prepsource}" >> $todo
    message "Wrote prepsource '$prepsource' to TODO: $todo"
    success "op-get -b $bibid $path"
fi

### EXIT
# http://stackoverflow.com/questions/430078/shell-script-templates
cleanup
trap 0
exit 0
