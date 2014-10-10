#!/usr/bin/env sh

DATA_DIR=`dirname $0`/data
SHUNIT_HELPER=`dirname $0`/shunit_helper

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
    cp -r $TEST_DATA_DIR/mscodex1223 $TEST_STAGING_DIR/mscodex1223
    op-prep medren $TEST_STAGING_DIR/mscodex1223
}

. $SHUNIT_HELPER
