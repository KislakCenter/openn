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
        mysql -u $OPENN_DB_USER openn_test -e "delete from $table"
    done
}

tearDown() {
    for table in openn_derivative openn_image openn_document
    do
        mysql -u $OPENN_DB_USER openn_test -e "delete from $table"
    done
    rm -rf $TEST_STAGING_DIR/* 2>/dev/null
}

testRun() {
    mysql -u $OPENN_DB_USER --default-character-set=utf8 openn_test < $THIS_DIR/fixtures/test.sql
    op-gen-pages
    status=$?
    assertEquals 0 $status
}


# Run shunit
. $shunit
