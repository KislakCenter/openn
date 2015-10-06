#!/usr/bin/env sh

THIS_DIR=`dirname $0`
source $THIS_DIR/shunit_helper

MS_COMPLETE=$TEST_DATA_DIR/mscodex1223_complete
ORIGINAL_TEI=$MS_COMPLETE/data/mscodex1223_TEI.xml

STAGED_DATA=$TEST_STAGING_DIR/mscodex1223
STAGED_TEI=$STAGED_DATA/data/mscodex1223_TEI.xml

SPREADSHEET_DATA_DIR=$TEST_DATA_DIR/diaries/haverford/MC_968_11_4_v03
SPREADSHEET_DATA_XLSX=$SPREADSHEET_DATA_DIR/openn_metadata.xlsx

# suite() {
#     suite_addTest testRun
#     # suite_addTest testSpreadsheet
#     # suite_addTest testOverWrite
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
    doc_id=`mysql -B -u openn openn_test --disable-column-names -e "select id from openn_document where base_dir = 'mscodex1223'"`
    output=`op-update-tei -o $TEST_STAGING_DIR penn-pih $doc_id 2>&1`
    status=$?
    [[ "$status" = 0 ]] || echo "$output"
    assertEquals 0 $status
    assertFalse "Should find PARTIAL_TEI.xml in $destdir; found `ls $TEST_STAGING_DIR/PARTIAL_TEI.xml 2>/dev/null`" "ls $TEST_STAGING_DIR/PARTIAL_TEI.xml"
}

testSpreadsheet() {
    mysql -u $OPENN_DB_USER --default-character-set=utf8 openn_test < $THIS_DIR/fixtures/test.sql
    doc_id=`mysql -B -u openn openn_test --disable-column-names -e "select id from openn_document where base_dir = 'MC_968_11_4_v03'"`
    # create the staging directory if needed
    [[ ! -d $TEST_STAGING_DIR ]] && mkdir $TEST_STAGING_DIR
    output=`op-update-tei -o $TEST_STAGING_DIR -k xlsx=$SPREADSHEET_DATA_XLSX haverford-diaries $doc_id 2>&1`
    status=$?
    [[ "$status" = 0 ]] || echo "$output"
    assertEquals 0 $status
    assertFalse "Should find PARTIAL_TEI.xml in $destdir; found `ls $TEST_STAGING_DIR/PARTIAL_TEI.xml 2>/dev/null`" "ls $TEST_STAGING_DIR/PARTIAL_TEI.xml"
}

testOverWrite() {
    # stage stuff
    mysql -u $OPENN_DB_USER --default-character-set=utf8 openn_test < $THIS_DIR/fixtures/test.sql
    doc_id=`mysql -B -u openn openn_test --disable-column-names -e "select id from openn_document where base_dir = 'mscodex1223'"`
    cp -r $MS_COMPLETE $STAGED_DATA

    # alter the staged version of the TEI
    echo >> $STAGED_TEI
    control_tei=$TEST_STAGING_DIR/control_tei.xml
    cp $STAGED_TEI $control_tei
    assertTrue "Control and staged TEI should be the same" "cmp $STAGED_TEI $control_tei"

    output=`op-update-tei -o $STAGED_DATA penn-pih $doc_id 2>&1`
    status=$?
    [[ "$status" = 0 ]] || echo "$output"
    assertEquals 0 $status
    assertTrue "TEI file should exist: $STAGED_TEI" "[ -f $STAGED_TEI ]"
    assertFalse "TEI file should be different from original" "cmp $ORIGINAL_TEI $control_tei"
    assertFalse "Should find PARTIAL_TEI.xml in $destdir; found `ls $TEST_STAGING_DIR/PARTIAL_TEI.xml 2>/dev/null`" "ls $TEST_STAGING_DIR/PARTIAL_TEI.xml"
}


# Run shunit
. $shunit
