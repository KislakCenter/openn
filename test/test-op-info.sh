#!/usr/bin/env sh

THIS_DIR=`dirname $0`
source $THIS_DIR/shunit_helper

# suite() {
#     suite_addTest testRun
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
    output=`op-info 2>&1`
    status=$?
    [[ "$status" = 0 ]] || echo "$output"
    assertEquals 0 $status
}

testCheckOnline() {
    loadDb
    output=`op-info --check-online 2>&1`
    status=$?
    [[ "$status" = 0 ]] || echo "$output"
    assertEquals 0 $status
}

testSetPrepsNoOp() {
    loadDb
    output=`op-info --set-preps 2>&1`
    status=$?
    [[ "$status" = 0 ]] || echo "$output"
    assertEquals 0 $status
}

testSetPrepsOneOnline() {
    loadDb
    mysql -u $OPENN_DB_USER $OPENN_DB_NAME -e "delete from openn_prepstatus"
    output=`op-info --set-preps 2>&1`
    status=$?
    [[ "$status" = 0 ]] || echo "$output"
    assertEquals 0 $status
}

testRepositories() {
    output=`op-info --repositories 2>&1`
    status=$?
    [[ "$status" = 0 ]] || echo "$output"
    assertEquals 0 $status
}

# Run shunit
. $shunit
