#!/usr/bin/env bash

################################################################################
#
# Generic wrapper for all OPenn python scripts.
#
# Collects the command (as -C SCRIPT.py); activates the virtualenv;
# runs the script; deactivates the virtualenv; returns the exit status
# of the called python script.
#
################################################################################

usage() {
    echo "Usage: `basename $0` SCRIPT.py ARGS"
    echo ""
    echo "Options"
    echo ""
    echo " -C <SCRIPT.py>   Name of the Python script to execute"
    echo
}

# SCRIPT NAME CHECK
# Do we have an arg?
if [ $# -lt 2 ]; then
    echo "Please provide a Python script path"
    usage
    exit 1
fi

if [ "$1" = "-C" ]; then
    :
else
    echo "Please provide a Python script path using the -C flag"
    usage
    exit 1
fi
shift

# Does the file exist?
if [ -f "$1" ]; then
    SCRIPT_PY="$1"
else
    echo "ERROR: Could not find Python script: $1"
    usage
    exit 1
fi

# shift arguments
shift

this_dir=`dirname $0`

# Virtualenv?
venv_dir=${this_dir}/../venv

if [ ! -d $venv_dir ]; then
    echo "ERROR: Cannot find required virtualenv dir: $venv_dir"
    exit 1
fi

source ${venv_dir}/bin/activate

python $SCRIPT_PY $@
status=$?

deactivate

exit $status
