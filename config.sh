#!/usr/bin/env bash

################################################################################
# Configure openn code
#
# - locate python v2.6|7
# - locate virtualenv
# - create virtualenv
# - install pyexiftool from demery github repo
#       - clone
#       - setup install
#       - delete clone repo
# - run pip install -r requirements.txt
#
# - print some helpful instructions

this_dir=`dirname $0`
cmd=`basenme $0`

usage() {
    echo "Usage: $cmd [OPTIONS]"
    echo ""
    echo "Options"
    echo ""
    echo " -h              print help and exit"
    echo " -e VIRTUALENV   Virtualenv executable"
    echo " -p PYTHON       Python executable"
    echo ""
}

find_python() {
    for fp_python in python python2.6 python26 python2.7 python27
    do
        echo "Testing python for version 2.[67].x: $fp_python" >&2
        if which $fp_python  >/dev/null 2>&1
        then
            fp_v=`python -V 2>&1`
            if [[ "$fp_v" =~ 2\.[67]\.[0-9] ]];
            then
                echo $fp_python
                return 0
                break
            else
                echo "Not the right python version: $fp_v" >&2
            fi
        fi
        fp_python=
        fp_v=
    done
    return 1
}

find_virtualenv() {
    for fv_virtualenv in virtualenv2.6 virtualenv26 virtualenv2.7 virtualenv27 virtualenv
    do
        echo "Testing virtualenv: $fv_virtualenv" >&2
        if which $fv_virtualenv  >/dev/null 2>&1
        then
            echo $fv_virtualenv
            return 0
            break
        else
            echo "Didn't find virtualenv: $fv_virtualenv"
        fi
        fv_virtualenv=
    done
    return 1
}


### OPTIONS
while getopts "hp:e:" opt; do
    case $opt in
        h)
            usage
            exit 1
            ;;
        p)
            OPENN_PYTHON=$OPTARG
            ;;
        e)
            OPENN_VIRTUALENV=$OPTARG
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


# - locate python v2.6|7
if [[ "$OPENN_PYTHON" ]]; then
    :
else
    OPENN_PYTHON=`find_python`
    if [[ $? -ne 0 ]]; then
        echo "Could not find python version 2.6.x or 2.7.x; quitting" >&2
        exit 1
    fi
fi
echo "Using python: $OPENN_PYTHON"

# - locate virtualenv
if [[ "$OPENN_VIRTUALENV" ]]; then
    :
else
    OPENN_VIRTUALENV=`find_virtualenv`
    if [[ $? -ne 0 ]]; thenf
        echo "Could not find virtualenv; quitting" >&2
        exit1
    fi
fi
echo "Using virtualenv: $OPENN_VIRTUALENV"

# # - create virtualenv
# if [[ -d $this_dir/venv ]]; then

# fi

# - install pyexiftool from demery github repo
#       - clone
#       - setup install
#       - delete clone repo
# - run pip install -r requirements.txt
#
# - print some helpful instructions
