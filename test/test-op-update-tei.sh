#!/usr/bin/env sh

THIS_DIR=`dirname $0`
source $THIS_DIR/shunit_helper

MS_COMPLETE=$TEST_DATA_DIR/mscodex1223_complete
ORIGINAL_TEI=$MS_COMPLETE/data/mscodex1223_TEI.xml

STAGED_DATA=$TEST_STAGING_DIR/mscodex1223
STAGED_TEI=$STAGED_DATA/data/mscodex1223_TEI.xml

# suite() {
#     # suite_addTest testRun
#     suite_addTest testOverWrite
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

testRun() {
    mysql -u $OPENN_DB_USER --default-character-set=utf8 openn_test < $THIS_DIR/fixtures/test.sql
    doc_id=`mysql -B -u openn openn --disable-column-names -e 'select max(id) from openn_document'`
    output=`op-update-tei -o $TEST_STAGING_DIR $doc_id 2>&1`
    status=$?
    [[ "$status" = 0 ]] || echo "$output"
    assertEquals 0 $status
}

testOverWrite() {
    # stage stuff
    mysql -u $OPENN_DB_USER --default-character-set=utf8 openn_test < $THIS_DIR/fixtures/test.sql
    doc_id=`mysql -B -u openn openn --disable-column-names -e 'select max(id) from openn_document'`
    cp -r $MS_COMPLETE $STAGED_DATA

    output=`op-update-tei -o $STAGED_DATA $doc_id 2>&1`
    status=$?
    [[ "$status" = 0 ]] || echo "$output"
    assertEquals 0 $status
    assertTrue "TEI file should exist: $STAGED_TEI" "[ -f $STAGED_TEI ]"
    assertFalse "TEI file should be different from original" "cmp $ORIGINAL_TEI $STAGED_TEI"
}


# Run shunit
. $shunit
