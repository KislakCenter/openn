#!/usr/bin/env sh

THIS_DIR=`dirname $0`
source $THIS_DIR/shunit_helper

DIR_EXTRA_IMAGES=$TEST_DATA_DIR/ljs454
PREPPED_DIR=$TEST_DATA_DIR/mscodex1223_prepped
TEMPLATE_TIFF=$TEST_IMAGE_DIR/template_image.tif
STAGING_DATA_DIR=$OPENN_STAGING_DIR/Data

# suite() {
#     # suite_addTest testRun
#     # suite_addTest testBloodyUnicode
#     # suite_addTest testStatusFlags
#     # suite_addTest testDocumentClobber
#     # suite_addTest testDocumentClobberCancel
#     # suite_addTest testDocumentClobberNoDocYet
#     # suite_addTest testDocumentClobberDocOnline
#     # suite_addTest testResume
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

# mc_968_11_4_v03_files="968_William_Allinson_v3_1.tif
#     968_William_Allinson_v3_2.tif
#     968_William_Allinson_v3_3.tif
#     968_William_Allinson_v3_4.tif
#     968_William_Allinson_v3_5.tif
#     968_William_Allinson_v3_6.tif
#     968_William_Allinson_v3_7.tif
#     968_William_Allinson_v3_8.tif
#     968_William_Allinson_v3_9.tif
#     968_William_Allinson_v3_10.tif
#     968_William_Allinson_v3_11.tif
#     968_William_Allinson_v3_12.tif
#     968_William_Allinson_v3_13.tif
#     968_William_Allinson_v3_14.tif
#     968_William_Allinson_v3_15.tif
#     968_William_Allinson_v3_16.tif
#     968_William_Allinson_v3_17.tif
#     968_William_Allinson_v3_18.tif
#     968_William_Allinson_v3_19.tif
#     968_William_Allinson_v3_20.tif
#     968_William_Allinson_v3_21.tif
#     968_William_Allinson_v3_22.tif
#     968_William_Allinson_v3_23.tif
#     968_William_Allinson_v3_24.tif
#     968_William_Allinson_v3_25.tif
#     968_William_Allinson_v3_26.tif
#     968_William_Allinson_v3_27.tif
#     968_William_Allinson_v3_28.tif
#     968_William_Allinson_v3_29.tif
#     968_William_Allinson_v3_30.tif
#     968_William_Allinson_v3_31.tif
#     968_William_Allinson_v3_32.tif
#     968_William_Allinson_v3_33.tif
#     968_William_Allinson_v3_34.tif
#     968_William_Allinson_v3_35.tif
#     968_William_Allinson_v3_36.tif
#     968_William_Allinson_v3_37.tif
#     968_William_Allinson_v3_38.tif"

testRun() {
    source_dir=$TEST_STAGING_DIR/mscodex1223
    cp -r $TEST_DATA_DIR/mscodex1223 $source_dir
    output=`op-prep penn-pih $source_dir`

    status=$?
    if [ $status != 0 ]
    then
        echo "$output"
    fi
    assertEquals 0 $status
    destdir=`get_staging_destination pennmss $source_dir`
    assertTrue "Expected TEI file in $destdir/data; found: `ls $destdir/data 2>/dev/null`" "ls $destdir/data/*[0-9]_TEI.xml"
    assertTrue "Expected manifest in $destdir" "[ -f $destdir/manifest-sha1.txt ]"
    assertTrue "Expected version.txt file in $destdir" "[ -f $destdir/version.txt ]"
    assertFalse "Should not find PIH XML in $destdir found: `ls $destdir/pih*.xml 2>/dev/null`" "ls $destdir/pih*.xml"
    assertFalse "Should not find file_list.json in $destdir; found: `ls $destdir/*.json 2>/dev/null`" "ls $destdir/*.json"
    assertFalse "Should find PARTIAL_TEI.xml in $destdir; found `ls $destdir/PARTIAL_TEI.xml 2>/dev/null`" "ls $destdir/PARTIAL_TEI.xml"

}

testResume() {
    # stage the data
    source_dir=$TEST_STAGING_DIR/mscodex1223
    cp -r $TEST_DATA_DIR/mscodex1223 $source_dir

    # make sure we fail
    # move some required files

    test_file=`ls $source_dir/*.tif | head -n 1`
    test_base=`basename $test_file`
    tmpdir=${TMPDIR:-/tmp}
    mv $test_file $tmpdir
    if [[ $? -ne 0 ]]; then
        exit 1
    fi
    output=`op-prep ljs-pih $source_dir 2>&1`
    status=$?
    if [ $status = 0 ]; then echo "$output"; fi
    assertNotEquals 0 $status

    # fix the problem and resume
    mv $tmpdir/$test_base $source_dir
    output=`op-prep -r ljs-pih $source_dir 2>&1`
    status=$?
    if [ $status != 0 ]; then echo "$output"; fi
    assertEquals 0 $status
}

testBloodyUnicode() {
    source_dir=$TEST_STAGING_DIR/ljs454
    cp -r $TEST_DATA_DIR/ljs454 $source_dir
    output=`op-prep ljs-pih $source_dir`
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
    output=`op-prep ljs-pih $package_dir`
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
    output=`op-prep penn-pih $package_dir`
    status=$?
    if [ $status != 0 ]
    then
        echo "$output"
    fi
    status=$?
    assertEquals 0 $status
    assertMatch "$output" "Repository prep already completed"
}

testDocumentClobber() {
    # set up the document
    insert_document MS_XYZ_1.2 haverford

    source_dir=$TEST_STAGING_DIR/MS_XYZ_1.2
    cp -r $TEST_DATA_DIR/sheets/valid_template $source_dir
    create_dummy_files $source_dir $dummy_files

    # now run clobber; should succeed
    output=`echo 'Yes' | op-prep --clobber haverford-diaries $source_dir 2>&1`
    status=$?
    if [ "$status" != 0 ]; then echo "$output"; fi
    assertEquals 0 "$status"
}

testDocumentClobberNoDocYet() {
    # set up the document
    source_dir=$TEST_STAGING_DIR/MS_XYZ_1.2
    cp -r $TEST_DATA_DIR/sheets/valid_template $source_dir
    touch_dummy_files $source_dir dummy_files
    output=`op-prep --clobber haverford-diaries $source_dir 2>&1`
    status=$?
    if [ "$status" = 0 ]; then echo "$output"; fi
    assertEquals 2 "$status"
    assertMatch "$output" "nonexistent document"
}

testDocumentClobberCancel() {
    # set up the document
    insert_document MS_XYZ_1.2 haverford
    source_dir=$TEST_STAGING_DIR/MS_XYZ_1.2
    cp -r $TEST_DATA_DIR/sheets/valid_template $source_dir
    touch_dummy_files $source_dir dummy_files

    # now cancel the clobber operation
    output=`echo 'No' | op-prep --clobber haverford-diaries $source_dir 2>&1`
    status=$?
    if [ "$status" = 0 ]; then echo "$output"; fi
    assertNotEquals 0 "$status"
    assertMatch "$output" "User canceled clobber"
}

testDocumentClobberDocOnline() {
    # set up the document
    insert_document MS_XYZ_1.2 haverford
    source_dir=$TEST_STAGING_DIR/MS_XYZ_1.2
    cp -r $TEST_DATA_DIR/sheets/valid_template $source_dir
    touch_dummy_files $source_dir dummy_files

    # set online flag to true
    sql="update openn_document set is_online = 1 where base_dir = 'MS_XYZ_1.2'"
    mysql -u $OPENN_DB_USER $OPENN_DB_NAME -e "$sql"

    # now it should break
    output=`op-prep --clobber haverford-diaries $source_dir 2>&1`
    status=$?
    if [ "$status" = 0 ]; then echo "$output"; fi
    assertNotEquals 0 "$status"
    assertMatch "$output" "document on-line"
}

# Run shunit
. $shunit
