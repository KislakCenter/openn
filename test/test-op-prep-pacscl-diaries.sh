#!/usr/bin/env sh

THIS_DIR=`dirname $0`
source $THIS_DIR/shunit_helper

DIR_EXTRA_IMAGES=$TEST_DATA_DIR/ljs454
PREPPED_DIR=$TEST_DATA_DIR/mscodex1223_prepped
TEMPLATE_TIFF=$TEST_IMAGE_DIR/template_image.tif
STAGING_DATA_DIR=$OPENN_STAGING_DIR/Data

# suite() {
#     # suite_addTest testRun
#     suite_addTest testSpreadsheetPrep
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

dummy_files="HelenGriffith_BMC_fc.tif
    HelenGriffith_BMC_fpd.tif
    HelenGriffith_BMC_0001.tif
    HelenGriffith_BMC_0002.tif
    HelenGriffith_BMC_0003.tif
    HelenGriffith_BMC_0004.tif
    HelenGriffith_BMC_0005.tif
    HelenGriffith_BMC_0006.tif
    HelenGriffith_BMC_0007.tif
    HelenGriffith_BMC_0008.tif
    HelenGriffith_BMC_0009.tif
    HelenGriffith_BMC_0010.tif
    HelenGriffith_BMC_0011.tif
    HelenGriffith_BMC_0012.tif
    HelenGriffith_BMC_0013.tif
    HelenGriffith_BMC_0014.tif
    HelenGriffith_BMC_0015.tif
    HelenGriffith_BMC_0016.tif
    HelenGriffith_BMC_0017.tif
    HelenGriffith_BMC_0018.tif"

mc_968_11_4_v03_files="968_William_Allinson_v3_1.tif
    968_William_Allinson_v3_2.tif
    968_William_Allinson_v3_3.tif
    968_William_Allinson_v3_4.tif
    968_William_Allinson_v3_5.tif
    968_William_Allinson_v3_6.tif
    968_William_Allinson_v3_7.tif
    968_William_Allinson_v3_8.tif
    968_William_Allinson_v3_9.tif
    968_William_Allinson_v3_10.tif
    968_William_Allinson_v3_11.tif
    968_William_Allinson_v3_12.tif
    968_William_Allinson_v3_13.tif
    968_William_Allinson_v3_14.tif
    968_William_Allinson_v3_15.tif
    968_William_Allinson_v3_16.tif
    968_William_Allinson_v3_17.tif
    968_William_Allinson_v3_18.tif
    968_William_Allinson_v3_19.tif
    968_William_Allinson_v3_20.tif
    968_William_Allinson_v3_21.tif
    968_William_Allinson_v3_22.tif
    968_William_Allinson_v3_23.tif
    968_William_Allinson_v3_24.tif
    968_William_Allinson_v3_25.tif
    968_William_Allinson_v3_26.tif
    968_William_Allinson_v3_27.tif
    968_William_Allinson_v3_28.tif
    968_William_Allinson_v3_29.tif
    968_William_Allinson_v3_30.tif
    968_William_Allinson_v3_31.tif
    968_William_Allinson_v3_32.tif
    968_William_Allinson_v3_33.tif
    968_William_Allinson_v3_34.tif
    968_William_Allinson_v3_35.tif
    968_William_Allinson_v3_36.tif
    968_William_Allinson_v3_37.tif
    968_William_Allinson_v3_38.tif"

testRun() {
    # mysql -u $OPENN_DB_USER --default-character-set=utf8 openn_test < $THIS_DIR/fixtures/test.sql
    source_dir=$TEST_STAGING_DIR/MC_968_11_4_v03
    cp -r $TEST_DATA_DIR/diaries/haverford/MC_968_11_4_v03 $source_dir
    create_dummy_files $source_dir $mc_968_11_4_v03_files
    output=`op-prep --verbose haverford-diaries $source_dir`
    status=$?
    if [ "$status" != 0 ]; then echo "$output"; fi
    assertEquals 0 "$status"
    destdir=`get_staging_destination haverford $source_dir`
    assertTrue "Expected destination dir $destdir" "[ -d $destdir ]"
    assertTrue "Expected TEI file in $destdir/data; found: `ls $destdir/data 2>/dev/null`" "ls $destdir/data/*_TEI.xml"
    assertTrue "Expected manifest in $destdir" "[ -f $destdir/manifest-sha1.txt ]"
    assertFalse "Should not find $destdir/openn_metadata.xml" "[ -f $destdir/openn_metadata.xml ]"
}


# Run shunit
. $shunit
