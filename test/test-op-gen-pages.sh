#!/usr/bin/env sh

THIS_DIR=`dirname $0`
source $THIS_DIR/shunit_helper

DIR_EXTRA_IMAGES=$TEST_DATA_DIR/mscodex1589

setUp() {
    if [ ! -d $TEST_STAGING_DIR ]; then
        mkdir $TEST_STAGING_DIR
    fi
    # make sure the database is empty
    for table in openn_derivative openn_image openn_document
    do
        mysql -u openn openn -e "delete from $table"
    done
}

tearDown() {
    for table in openn_derivative openn_image openn_document
    do
        mysql -u openn openn -e "delete from $table"
    done
    rm -rf $TEST_STAGING_DIR/* 2>/dev/null
}

testRun() {
    mysql -uopenn --default-character-set=utf8 openn < $THIS_DIR/fixtures/test.sql
    op-gen-pages
    status=$?
    assertEquals 0 $status
}


# Run shunit
. $shunit
