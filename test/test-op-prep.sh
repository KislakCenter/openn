#!/usr/bin/env sh

source `dirname $0`/shunit_helper

DIR_EXTRA_IMAGES=$TEST_DATA_DIR/ljs454
PREPPED_DIR=$TEST_DATA_DIR/mscodex1223_prepped

setUp() {
    if [ ! -d $TEST_STAGING_DIR ]; then
        mkdir $TEST_STAGING_DIR
    fi
    # make sure the database is empty
    clear_tables
}

# suite() {
#     suite_addTest testRun
#     # suite_addTest testBloodyUnicode
#     # suite_addTest testStatusFlags
# }

tearDown() {
    clear_tables
    rm -rf $TEST_STAGING_DIR/* 2>/dev/null
}

testRun() {
    source_dir=$TEST_STAGING_DIR/mscodex1223
    cp -r $TEST_DATA_DIR/mscodex1223 $source_dir
    output=`op-prep medren $source_dir`

    # source_dir=$TEST_STAGING_DIR/mscodex1589
    # cp -r $TEST_DATA_DIR/mscodex1589 $source_dir
    # source=`op-prep medren $source_dir`

    # source_dir=$TEST_STAGING_DIR/ljs454
    # cp -r $TEST_DATA_DIR/ljs454 $source_dir
    # output=`op-prep ljs $source_dir`

    status=$?
    if [ $status != 0 ]
    then
        echo "$output"
    fi
    assertEquals 0 $status
    assertTrue "Expected TEI file in $source_dir/data; found: `ls $source_dir/data 2>/dev/null`" "ls $source_dir/data/*[0-9]_TEI.xml"
    assertTrue "Expected manifest in $source_dir" "[ -f $source_dir/manifest-sha1.txt ]"
    assertTrue "Expected version.txt file in $source_dir" "[ -f $source_dir/version.txt ]"
    assertFalse "Should not find PIH XML in $source_dir found: `ls $source_dir/pih*.xml 2>/dev/null`" "ls $source_dir/pih*.xml"
    assertFalse "Should not find file_list.json in $source_dir; found: `ls $source_dir/*.json 2>/dev/null`" "ls $source_dir/*.json"
    assertFalse "Should find PARTIAL_TEI.xml in $source_dir; found `ls $source_dir/PARTIAL_TEI.xml 2>/dev/null`" "ls $source_dir/PARTIAL_TEI.xml"
}

testResume() {
    # stage the data
    source_dir=$TEST_STAGING_DIR/mscodex1223
    cp -r $TEST_DATA_DIR/mscodex1223 $source_dir

    # make sure we fail
    touch $source_dir/somebadilfe.txt
    output=`op-prep ljs $source_dir 2>&1`
    status=$?
    if [ $status = 0 ]; then echo "$output"; fi
    assertNotEquals 0 $status
    assertMatch "$output" "VALID NAME CHECK"

    # fix the problem and resume
    rm $source_dir/somebadilfe.txt
    output=`op-prep -r ljs $source_dir 2>&1`
    status=$?
    if [ $status != 0 ]; then echo "$output"; fi
    assertEquals 0 $status
}

testBloodyUnicode() {
    source_dir=$TEST_STAGING_DIR/ljs454
    cp -r $TEST_DATA_DIR/ljs454 $source_dir
    output=`op-prep ljs $source_dir`
    status=$?
    if [ $status != 0 ]
    then
        echo "$output"
    fi
    # source_dir=$TEST_STAGING_DIR/mscodex1589
    # cp -r $TEST_DATA_DIR/mscodex1589 $source_dir
    # op-prep medren $source_dir
    status=$?
    assertEquals 0 $status
}

testImagesNotInPIH() {

    package_dir=$TEST_STAGING_DIR/ljs454
    cp -r $DIR_EXTRA_IMAGES $package_dir
    output=`op-prep ljs $package_dir`
    status=$?
    if [ $status != 0 ]
    then
        echo "$output"
    fi
    status=$?
    assertEquals 0 $status
}

testStatusFlags() {
    package_dir=$TEST_STAGING_DIR/mscodex1223
    cp -r $PREPPED_DIR $package_dir
    output=`op-prep medren $package_dir`
    status=$?
    if [ $status != 0 ]
    then
        echo "$output"
    fi
    status=$?
    assertEquals 0 $status
    assertMatch "$output" "Collection prep already completed"
}

# Run shunit
. $shunit
