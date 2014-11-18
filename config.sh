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
this_dir=$( cd $this_dir; pwd )
cmd=`basename $0`

PYEXIFTOOL_GIT=git@github.com:demery/pyexiftool.git

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
            fp_v=`$fp_python -V 2>&1`
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
    fv_virtualenvs="
virtualenv2.6
virtualenv26
virtualenv2.7
virtualenv27
virtualenv-2.6
virtualenv-26
virtualenv-2.7
virtualenv-27
virtualenv
"
    for fv_virtualenv in $fv_virtualenvs
    do
        echo "Testing virtualenv: $fv_virtualenv" >&2
        if which $fv_virtualenv  >/dev/null 2>&1
        then
            echo $fv_virtualenv
            return 0
            break
        else
            echo "Didn't find virtualenv: $fv_virtualenv" >&2
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
            echo
            usage
            exit 1
            ;;
    esac
done

shift $((OPTIND-1))


# - locate python v2.6|7
if [[ "$OPENN_PYTHON" ]]
then
    :
else
    OPENN_PYTHON=`find_python`
    if [[ $? -ne 0 ]]
then
        echo "[$cmd] Could not find python version 2.6.x or 2.7.x; quitting" >&2
        exit 1
    fi
fi
echo "[$cmd] Using python: $OPENN_PYTHON"

# - locate virtualenv
if [[ "$OPENN_VIRTUALENV" ]]
then
    :
else
    OPENN_VIRTUALENV=`find_virtualenv`
    if [[ $? -ne 0 ]]
        then
        echo "[$cmd] Could not find virtualenv; quitting" >&2
        exit1
    fi
fi
echo "[$cmd] Using virtualenv: $OPENN_VIRTUALENV"

# - create virtualenv
venv_dir=$this_dir/venv
if [[ -d $venv_dir ]]
then
    echo "[$cmd] ERROR: Pffft! $venv_dir already exists; I'm quitting." >&2
    exit 1
fi

$OPENN_VIRTUALENV --python=$OPENN_PYTHON --prompt="(openn-prodn)" $venv_dir
if [[ $? -ne 0 ]]
then
    echo "[$cmd] ERROR: Error creating virtualenv at: $venv_dir" >&2
    exit 1
fi

source $venv_dir/bin/activate

# make sure python in expected path
which_python=`which python`
if [[ "$which_python" = $venv_dir/bin/python ]]
then
    :
else
    echo "[$cmd] ERROR: Expected python at $venv_dir/bin/python; found: $which_python" >&2
    exit 1
fi

# - install pyexiftool from demery github repo
#       - clone
clone_dir=$this_dir/pyexiftool
if [[ -d $clone_dir ]]
then
    echo "[$cmd] ERROR: pyexiftool directory already exists: $clone_dir"
    exit 1
fi
git clone $PYEXIFTOOL_GIT $clone_dir

# - install pyexiftool from demery github repo
#       - setup install
curr_dir=`pwd`
cd $clone_dir

if python setup.py install
then
    :
else
    echo "[$cmd] Error installing pyexiftool" >&2
    exit 1
fi

echo "[$cmd] pyexiftool installed"

if [[ `pwd` =~ pyexiftool$ ]]
then
    find . -delete
else
    echo "[$cmd] ERROR: Should be in pyexiftool directory; found: `pwd`" >&2
    exit 1
fi

if cd $curr_dir
then
    if rmdir pyexiftool
    then
        :
    else
        echo "[$cmd] ERROR: Error removing pyexiftool" >&2
        exit 1
    fi
fi

echo "[$cmd] Running pip install -r requirements.txt"
# - run pip install -r requirements.txt
reqs_txt=$this_dir/requirements.txt
if [[ -f $reqs_txt ]]
then
    :
else
    echo "[$cmd] ERROR: requirements.txt not found: $reqs_txt" >&2
    exit 1
fi
pip install -r $reqs_txt
if [[ $? -eq 0 ]]
then
    echo "[$cmd] Libraries installed"
else
    echo "[$cmd] ERROR: Problem installing required libraries" >&2
    exit 1
fi

# secret
secret_txt=$this_dir/openn/secret_key.txt
if [[ -f $secret_txt ]]
then
    echo "[$cmd] Found secret: $secret_txt"
else
    echo "[$cmd] Creating secret file: $secret_txt"
    LC_CTYPE=C tr -dc A-Za-z0-9_\!\@\#\$\%\^\&\*\(\)-+= < /dev/urandom | head -c 50 | xargs > $secret_txt
fi

#
# - print some helpful instructions
openn_bin=$this_dir/bin
echo
echo "[$cmd] ============================================================"
echo "[$cmd]"
echo "[$cmd] SUCCESS! OPenn scripts are configured"
echo "[$cmd] Be sure to add the OPenn scripts to your path:"
echo "[$cmd]"
echo "[$cmd]      export PATH=$openn_bin:\$PATH"
echo "[$cmd]"
echo "[$cmd] ============================================================"
echo
