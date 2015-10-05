#!/usr/bin/env sh

source `dirname $0`/shunit_helper

DIR_EXTRA_IMAGES=$TEST_DATA_DIR/ljs454
PREPPED_DIR=$TEST_DATA_DIR/mscodex1223_prepped
TEMPLATE_TIFF=$TEST_IMAGE_DIR/template_image.tif
STAGING_DATA_DIR=$OPENN_STAGING_DIR/Data

setUp() {
    if [ ! -d $TEST_STAGING_DIR ]; then
        mkdir $TEST_STAGING_DIR
    fi
    # make sure the database is empty
    clear_tables
}

# suite() {
#     suite_addTest testRun
#     # suite_addTest testSpreadsheetPrep
#     # suite_addTest testBloodyUnicode
#     # suite_addTest testStatusFlags
#     # suite_addTest testDocumentClobber
#     # suite_addTest testDocumentClobberCancel
#     # suite_addTest testDocumentClobberNoDocYet
#     # suite_addTest testDocumentClobberDocOnline
#     # suite_addTest testResume
# }

get_collection_id() {
    gci_tag=${1?get_collection_id - tag required}
    gci_id=`mysql --batch --skip-column-names -u openn openn -e "select id from openn_openncollection where tag = '$gci_tag'"`
    [[ -z "$gci_id" ]] && return 1
    echo $gci_id
    return 0
}

get_collection_folder() {
    gcf_id=`get_collection_id $1`
    [[ -z "$gcf_id" ]] && return 1
    printf "%04d\n" $gcf_id
    return 0
}

get_staging_destination() {
    gsd_folder=`get_collection_folder $1`
    gsd_source_dir=$2
    [[ -z "$gsd_folder" ]] && return 1
    [[ -z "$gsd_source_dir" ]] && return 1
    echo $STAGING_DATA_DIR/$gsd_folder/`basename $gsd_source_dir`
    return 0
}

insert_document() {
    today=`date "+%Y-%m-%d"`
    haverford_id=`get_collection_id  haverford` || {
        echo  "ERROR: haverford not in collections table";
        exit 1; }
    sql="insert into openn_document"
    sql="$sql (openn_collection_id, base_dir, is_online, created, updated)"
    sql="$sql values ($haverford_id, 'MS_XYZ_1.2', 0, '$today', '$today')"
    mysql -u $OPENN_DB_USER $OPENN_DB_NAME -e "$sql"
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

touch_dummy_files() {
    tdf_dest_dir=$1
    if [[ -z "$tdf_dest_dir" ]] || [[ ! -d $tdf_dest_dir ]]; then
        echo "[create_dummy_files] Directory not found: '$tdf_dest_dir'; quitting"
        exit 1
    fi
    for x in $dummy_files; do
        touch "$tdf_dest_dir/$x"
    done
}

create_dummy_files() {
    cdf_dest_dir=$1
    if [[ -z "$cdf_dest_dir" ]] || [[ ! -d $cdf_dest_dir ]]; then
        echo "[create_dummy_files] Directory not found: '$cdf_dest_dir'; quitting"
        exit 1
    fi
    for x in $dummy_files; do
        cp $TEMPLATE_TIFF "$cdf_dest_dir/$x"
    done
}

testRun() {
    source_dir=$TEST_STAGING_DIR/mscodex1223
    cp -r $TEST_DATA_DIR/mscodex1223 $source_dir
    output=`op-prep penn-pih $source_dir`

    # source_dir=$TEST_STAGING_DIR/mscodex1589
    # cp -r $TEST_DATA_DIR/mscodex1589 $source_dir
    # source=`op-prep medren $source_dir`

    # source_dir=$TEST_STAGING_DIR/ljs454
    # cp -r $TEST_DATA_DIR/ljs454 $source_dir
    # output=`op-prep ljs $source_dir`

    # source_dir=$TEST_STAGING_DIR/MS_XYZ_1.2
    # cp -r $TEST_DATA_DIR/sheets/valid_template $source_dir
    # create_dummy_files $source_dir
    # output=`op-prep haverford $source_dir`
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

testSpreadsheetPrep() {
    source_dir=$TEST_STAGING_DIR/MS_XYZ_1.2
    cp -r $TEST_DATA_DIR/sheets/valid_template $source_dir
    create_dummy_files $source_dir
    output=`op-prep haverford-diaries $source_dir`
    status=$?
    if [ "$status" != 0 ]; then echo "$output"; fi
    assertEquals 0 "$status"
    destdir=`get_staging_destination haverford $source_dir`
    assertTrue "Expected destination dir $destdir" "[ -d $destdir ]"
    assertTrue "Expected TEI file in $destdir/data; found: `ls $destdir/data 2>/dev/null`" "ls $destdir/data/*_TEI.xml"
    assertTrue "Expected manifest in $destdir" "[ -f $destdir/manifest-sha1.txt ]"
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
    assertMatch "$output" "Collection prep already completed"
}

testDocumentClobber() {
    # set up the document
    insert_document

    source_dir=$TEST_STAGING_DIR/MS_XYZ_1.2
    cp -r $TEST_DATA_DIR/sheets/valid_template $source_dir
    create_dummy_files $source_dir

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
    touch_dummy_files $source_dir
    output=`op-prep --clobber haverford-diaries $source_dir 2>&1`
    status=$?
    if [ "$status" = 0 ]; then echo "$output"; fi
    assertEquals 2 "$status"
    assertMatch "$output" "nonexistent document"
}

testDocumentClobberCancel() {
    # set up the document
    insert_document
    source_dir=$TEST_STAGING_DIR/MS_XYZ_1.2
    cp -r $TEST_DATA_DIR/sheets/valid_template $source_dir
    touch_dummy_files $source_dir

    # now cancel the clobber operation
    output=`echo 'No' | op-prep --clobber haverford-diaries $source_dir 2>&1`
    status=$?
    if [ "$status" = 0 ]; then echo "$output"; fi
    assertNotEquals 0 "$status"
    assertMatch "$output" "User canceled clobber"
}

testDocumentClobberDocOnline() {
    # set up the document
    insert_document
    source_dir=$TEST_STAGING_DIR/MS_XYZ_1.2
    cp -r $TEST_DATA_DIR/sheets/valid_template $source_dir
    touch_dummy_files $source_dir

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
