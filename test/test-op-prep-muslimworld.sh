#!/usr/bin/env sh

THIS_DIR=`dirname $0`
source $THIS_DIR/shunit_helper

TEMPLATE_TIFF=$TEST_IMAGE_DIR/template_image.tif
STAGING_DATA_DIR=$OPENN_STAGING_DIR/Data

# suite() {
#     suite_addTest testRun
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

COLUMBIA_ms_or_15="ms_or_15_000_0000001.tif
        ms_or_15_000_0000002.tif
        ms_or_15_000_0000003.tif
        ms_or_15_000_0000004.tif
        ms_or_15_000_0000005.tif
        ms_or_15_000_0000006.tif
        ms_or_15_000_0000007.tif
        ms_or_15_000_0000008.tif
        ms_or_15_000_0000009.tif
        ms_or_15_000_0000010.tif
        ms_or_15_000_0000011.tif
        ms_or_15_000_0000012.tif
        ms_or_15_000_0000013.tif
        ms_or_15_000_0000014.tif
        ms_or_15_000_0000015.tif
        ms_or_15_000_0000016.tif"

testRun() {
    loadDb
    name_dir=ms_or_15
    source_dir=${TEST_STAGING_DIR}/$name_dir
    template_dir=${TEST_DATA_DIR}/muslim_world/$name_dir
    cp -r $template_dir $source_dir
    create_dummy_files $source_dir $COLUMBIA_ms_or_15
    output=`op-prep columbia-mmw $source_dir`
    status=$?
    if [ "$status" != 0 ]; then echo "$output"; fi

    assertEquals 0 "$status"
    destdir=`get_staging_destination columbia $source_dir`
    # save_and_open "$destdir/data/${name_dir}_TEI.xml"
    assertTrue "Expected destination dir $destdir" "[ -d $destdir ]"
    assertTrue "Expected TEI file in $destdir/data; found: `ls $destdir/data 2>/dev/null`" "ls $destdir/data/${name_dir}_TEI.xml"
    assertTrue "Expected manifest in $destdir" "[ -f $destdir/manifest-sha1.txt ]"
    assertFalse "Should not find $destdir/openn_metadata.xml" "[ -f $destdir/marc.xml ]"
}



# Run shunit
. $shunit
