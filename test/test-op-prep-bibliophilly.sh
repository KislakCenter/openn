#!/usr/bin/env sh

THIS_DIR=`dirname $0`
source $THIS_DIR/shunit_helper

TEMPLATE_TIFF=$TEST_IMAGE_DIR/template_image.tif
STAGING_DATA_DIR=$OPENN_STAGING_DIR/Data

# suite() {
#     # suite_addTest testRun
# }

setUp() {
    rm -rf $TEST_STAGING_DIR/* 2>/dev/null
    if [ ! -d $TEST_STAGING_DIR ]; then
        mkdir $TEST_STAGING_DIR
    fi
    # make sure the database is empty
    clear_tables
}

tearDown() {
    clear_tables
    # rm -rf $TEST_STAGING_DIR/* 2>/dev/null
}

DUMMY_FILES="lewis_e_087_body0001.tif
lewis_e_087_body0002.tif
lewis_e_087_body0003.tif
lewis_e_087_body0004.tif
lewis_e_087_body0005.tif
lewis_e_087_body0006.tif
lewis_e_087_body0007.tif
lewis_e_087_body0008.tif
lewis_e_087_body0009.tif
lewis_e_087_body0010.tif
lewis_e_087_body0011.tif
lewis_e_087_body0012.tif
lewis_e_087_body0013.tif
lewis_e_087_body0014.tif
lewis_e_087_body0015.tif
lewis_e_087_body0016.tif
lewis_e_087_body0017.tif
lewis_e_087_body0018.tif"

testRun() {
    loadDb
    source_dir=${TEST_STAGING_DIR}/FLPLewisE087
    template_dir=${TEST_DATA_DIR}/bibliophilly/FLPLewisE087
    cp -r $template_dir $source_dir
    create_dummy_files $source_dir $DUMMY_FILES

    output=`op-prep flp-bphil $source_dir`
    status=$?
    if [ "$status" != 0 ]; then echo "$output"; fi
    # echo "$output"
    # find $TEST_STAGING_DIR
    # save_and_open "${TEST_STAGING_DIR}/FLPLewisE087/PARTIAL_TEI.xml" "Sublime Text"

    assertEquals 0 "$status"
    destdir=`get_staging_destination flp $source_dir`
    assertTrue "Expected destination dir $destdir" "[ -d $destdir ]"
    assertTrue "Expected TEI file in $destdir/data; found: `ls $destdir/data 2>/dev/null`" "ls $destdir/data/*_TEI.xml"
    assertTrue "Expected manifest in $destdir" "[ -f $destdir/manifest-sha1.txt ]"
    assertFalse "Should not find $destdir/openn_metadata.xml" "[ -f $destdir/openn_metadata.xml ]"
}

# Run shunit
. $shunit
