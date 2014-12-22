#!/usr/bin/env sh

THIS_DIR=`dirname $0`
source $THIS_DIR/shunit_helper

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

testRun() {
    mysql -u $OPENN_DB_USER --default-character-set=utf8 openn_test < $THIS_DIR/fixtures/test.sql
    doc_id=`mysql -B -u openn openn --disable-column-names -e 'select max(id) from openn_document'`
    op-update-tei -o $TEST_STAGING_DIR $doc_id
    status=$?
    assertEquals 0 $status
}


# Run shunit
. $shunit
