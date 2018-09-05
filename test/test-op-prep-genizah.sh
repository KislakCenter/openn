#!/usr/bin/env sh

THIS_DIR=`dirname $0`
source $THIS_DIR/shunit_helper

TEMPLATE_TIFF=$TEST_IMAGE_DIR/template_image.tif
STAGING_DATA_DIR=$OPENN_STAGING_DIR/Data

# suite() {
#     # suite_addTest testRun
#     # suite_addTest testLewis_e_003
#     # suite_addTest testLewis_e_005
#     # suite_addTest testLewis_e_009
#     suite_addTest testLewis_e_049
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
    rm -rf $TEST_STAGING_DIR/* 2>/dev/null
}

DUMMY_FILES="h001_wk1_body0001.tif
h001_wk1_body0002.tif"

testRun() {
    loadDb
    name_dir=h001
    source_dir=${TEST_STAGING_DIR}/$name_dir
    template_dir=${TEST_DATA_DIR}/genizah/$name_dir
    cp -r $template_dir $source_dir
    create_dummy_files $source_dir $DUMMY_FILES

    output=`op-prep penn-gzh $source_dir`
    status=$?
    if [ "$status" != 0 ]; then echo "$output"; fi


    assertEquals 0 "$status"
    destdir=`get_staging_destination pennmss $source_dir`
    # save_and_open "$destdir/data/${name_dir}_TEI.xml"
    assertTrue "Expected destination dir $destdir" "[ -d $destdir ]"
    assertTrue "Expected TEI file in $destdir/data; found: `ls $destdir/data 2>/dev/null`" "ls $destdir/data/${name_dir}_TEI.xml"
    assertTrue "Expected manifest in $destdir" "[ -f $destdir/manifest-sha1.txt ]"
    assertFalse "Should not find $destdir/openn_metadata.xml" "[ -f $destdir/openn_metadata.xml ]"
}


# Run shunit
. $shunit
