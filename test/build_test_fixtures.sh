#!/usr/bin/env bash

this_dir=`dirname $0`

# Only run on the dev machine; not in production or anywhere else
EXPECTED_HOST=rbm-dxe02.library.upenn.edu
ACTUAL_HOST=`hostname`
if [[ $EXPECTED_HOST = $ACTUAL_HOST ]]; then
    echo "On dev machine continuing"
else
    echo "ERROR: Only running on dev machine; expected host: $EXPECTED_HOST; found $ACTUAL_HOST"
    exit 1
fi

# not running tests; but there's a lot other useful stuff in
# shunit_helper; like:
#
# export PATH=`dirname $0`/../bin:$PATH
# export TEST_DATA_DIR=`dirname $0`/../openn/tests/data
# export TEST_STAGING_DIR=`dirname $0`/../openn/tests/staging
#
# export OPENN_DB_NAME=openn_test
# export OPENN_DB_USER=openn
# export OPENN_DB_HOST=localhost
# export OPENN_PACKAGE_DIR=$TEST_STAGING_DIR/openn/packages
# export OPENN_STAGING_DIR=$TEST_STAGING_DIR/openn/site
source `dirname $0`/shunit_helper

# backup the current dev database
backup_file=openn_`date +%Y%m%dT%H%M%S%z`.dmp
if mysqldump -u openn openn >  $backup_file; then
    echo "INFO: Backed up datase openn to $backup_file"
else
    echo "ERROR: Unable to backup database; quitting"
fi

# clear the test database
clear_tables

sources="mscodex1223:medren mscodex1589:medren ljs454:ljs"

# load the test database with real data
for src in $sources
do
    dir=`echo $src | awk -F ':' '{ print $1 }'`
    coll=`echo $src |awk -F ':' '{ print $2 }'`

    source_dir=$TEST_STAGING_DIR/$dir
    cp -r $TEST_DATA_DIR/$dir $source_dir
    # echo "source_dir is $source_dir"
    echo "INFO: Running: op-prep $coll $source_dir"
    output=`op-prep $coll $source_dir`
    if [[ $? -ne 0 ]]; then
        echo "ERROR: Problem running op-prep"
        echo "$output"
        exit 1
    fi
done

# export the test database
TEST_SQL=$this_dir/fixtures/test.sql
mysqldump -u openn openn_test > $TEST_SQL

# clear the test database
clear_tables
# delete the staged data
rm -rf $TEST_STAGING_DIR/*

# load the test data into openn
mysql -u openn openn < $TEST_SQL

# dump the data
OPENN_DB_NAME=openn TEST_JSON=$this_dir/../openn/fixtures/test.json
$this_dir/../manage.py dumpdata > $TEST_JSON

# rebuild the database
mysql -u openn -e "drop database openn"
mysql -u openn -e "CREATE DATABASE openn CHARACTER SET utf8 COLLATE utf8_unicode_ci;"
OPENN_DB_NAME=openn $this_dir/../manage.py  syncdb
OPENN_DB_NAME=openn $this_dir/../manage.py  migrate

# run git status to show what's changed
git status
