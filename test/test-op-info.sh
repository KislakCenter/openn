#!/usr/bin/env sh

THIS_DIR=`dirname $0`
source $THIS_DIR/shunit_helper


# suite() {
#     suite_addTest testForce
# }

setUp() {
    if [ ! -d $TEST_STAGING_DIR ]; then
        mkdir $TEST_STAGING_DIR
    fi
    # make sure the database is empty
    clear_tables
}

tearDown() {
    clear_tables
    rm -rf $TEST_STAGING_DIR/* 2>/dev/null
}

loadDb() {
    mysql -u $OPENN_DB_USER --default-character-set=utf8 openn_test < $THIS_DIR/fixtures/test.sql
}

stagePages() {
    # make sure the staged data isn't there
    rm -rf $STAGED_DATA
    cp -r $TEMPLATE_PAGES $STAGED_PAGES
}

testRun() {
    loadDb
    op-info
    status=$?
    # if [ $status != 0 ]; then echo "$output"; fi
    assertEquals 0 $status
}

testCheckOline() {
    loadDb
    op-info --check-online
    status=$?
    # if [ $status != 0 ]; then echo "$output"; fi
    assertEquals 0 $status
}

# Run shunit
. $shunit
