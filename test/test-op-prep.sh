#!/usr/bin/env sh

source `dirname $0`/shunit_helper

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

# suite() {
#     suite_addTest testRun
# }

tearDown() {
    for table in openn_derivative openn_image openn_document
    do
        mysql -u openn openn -e "delete from $table"
    done
    rm -rf $TEST_STAGING_DIR/* 2>/dev/null
}

testRun() {
    source_dir=$TEST_STAGING_DIR/mscodex1223
    cp -r $TEST_DATA_DIR/mscodex1223 $source_dir
    op-prep medren $source_dir
    status=$?
    assertEquals 0 $status
    assertTrue "Expected TEI file in $source_dir/data; found: `ls $source_dir/data 2>/dev/null`" "ls $source_dir/data/*[0-9]_TEI.xml"
    assertFalse "Should not find PIH XML in $source_dir found: `ls $source_dir/pih*.xml 2>/dev/null`" "ls $source_dir/pih*.xml"
    assertFalse "Should not find file_list.json in $source_dir; found: `ls $source_dir/*.json 2>/dev/null`" "ls $source_dir/*.json"
    assertFalse "Should find PARTIAL_TEI.xml in $source_dir; found `ls $source_dir/PARTIAL_TEI.xml 2>/dev/null`" "ls $source_dir/PARTIAL_TEI.xml"
}

testImagesNotInPIH() {

    package_dir=$TEST_STAGING_DIR/mscodex1589
    cp -r $DIR_EXTRA_IMAGES $package_dir
    op-prep medren $package_dir
    status=$?
    assertEquals 0 $status
}

# Run shunit
. $shunit