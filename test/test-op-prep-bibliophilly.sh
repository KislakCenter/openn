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

LEWIS_E_003_FILES="lewis_e_003_body0001.tif
lewis_e_003_body0002.tif
lewis_e_003_body0003.tif
lewis_e_003_body0004.tif
lewis_e_003_body0005.tif
lewis_e_003_body0006.tif
lewis_e_003_body0007.tif
lewis_e_003_body0008.tif
lewis_e_003_body0009.tif
lewis_e_003_body0010.tif
lewis_e_003_body0027.tif
lewis_e_003_body0028.tif
lewis_e_003_body0035.tif
lewis_e_003_body0036.tif
lewis_e_003_body0037.tif
lewis_e_003_body0038.tif
lewis_e_003_body0041.tif
lewis_e_003_body0042.tif
lewis_e_003_body0045.tif
lewis_e_003_body0046.tif
lewis_e_003_body0071.tif
lewis_e_003_body0072.tif
lewis_e_003_body0073.tif
lewis_e_003_body0074.tif
lewis_e_003_body0075.tif
lewis_e_003_body0076.tif
lewis_e_003_body0077.tif
lewis_e_003_body0078.tif
lewis_e_003_body0079.tif
lewis_e_003_body0080.tif
lewis_e_003_body0087.tif
lewis_e_003_body0088.tif
lewis_e_003_body0089.tif
lewis_e_003_body0090.tif
lewis_e_003_body0091.tif
lewis_e_003_body0092.tif
lewis_e_003_body0093.tif
lewis_e_003_body0094.tif"

LEWIS_E_005_FILES="lewis_e_005_body0001.tif
lewis_e_005_body0002.tif
lewis_e_005_body0003.tif
lewis_e_005_body0004.tif
lewis_e_005_body0005.tif
lewis_e_005_body0006.tif
lewis_e_005_body0007.tif
lewis_e_005_body0008.tif
lewis_e_005_body0009.tif
lewis_e_005_body0010.tif
lewis_e_005_body0019.tif
lewis_e_005_body0020.tif
lewis_e_005_body0021.tif
lewis_e_005_body0022.tif
lewis_e_005_body0023.tif
lewis_e_005_body0024.tif
lewis_e_005_body0041.tif
lewis_e_005_body0042.tif
lewis_e_005_body0043.tif
lewis_e_005_body0044.tif
lewis_e_005_body0045.tif
lewis_e_005_body0046.tif
lewis_e_005_body0047.tif
lewis_e_005_body0048.tif
"

LEWIS_E_009_FILES="lewis_e_009_body0001.tif
lewis_e_009_body0002.tif
lewis_e_009_body0003.tif
lewis_e_009_body0004.tif
lewis_e_009_body0005.tif
lewis_e_009_body0006.tif
lewis_e_009_body0025.tif
lewis_e_009_body0026.tif
lewis_e_009_body0027.tif
lewis_e_009_body0028.tif
lewis_e_009_body0029.tif
lewis_e_009_body0030.tif
lewis_e_009_body0031.tif
lewis_e_009_body0032.tif
lewis_e_009_body0033.tif
lewis_e_009_body0034.tif
lewis_e_009_body0105.tif
lewis_e_009_body0106.tif
lewis_e_009_body0107.tif
lewis_e_009_body0108.tif
lewis_e_009_body0109.tif
lewis_e_009_body0110.tif
lewis_e_009_body0111.tif
lewis_e_009_body0112.tif
lewis_e_009_body0113.tif
lewis_e_009_body0114.tif
lewis_e_009_body0115.tif
lewis_e_009_body0116.tif
lewis_e_009_body0117.tif
lewis_e_009_body0118.tif"

LEWIS_E_049_FILES="lewis_e_049_body0001.tif
lewis_e_049_body0002.tif
lewis_e_049_body0003.tif
lewis_e_049_body0004.tif
lewis_e_049_body0005.tif
lewis_e_049_body0006.tif
lewis_e_049_body0143.tif
lewis_e_049_body0144.tif
lewis_e_049_body0145.tif
lewis_e_049_body0146.tif
lewis_e_049_body0147.tif
lewis_e_049_body0148.tif
lewis_e_049_body0159.tif
lewis_e_049_body0160.tif
lewis_e_049_body0161.tif
lewis_e_049_body0162.tif
lewis_e_049_body0163.tif
lewis_e_049_body0164.tif"

testRun() {
    loadDb
    name_dir=FLPLewisE087
    source_dir=${TEST_STAGING_DIR}/$name_dir
    template_dir=${TEST_DATA_DIR}/bibliophilly/$name_dir
    cp -r $template_dir $source_dir
    create_dummy_files $source_dir $DUMMY_FILES

    output=`op-prep flp-bphil $source_dir`
    status=$?
    if [ "$status" != 0 ]; then echo "$output"; fi


    assertEquals 0 "$status"
    destdir=`get_staging_destination flp $source_dir`
    # save_and_open "$destdir/data/${name_dir}_TEI.xml"
    assertTrue "Expected destination dir $destdir" "[ -d $destdir ]"
    assertTrue "Expected TEI file in $destdir/data; found: `ls $destdir/data 2>/dev/null`" "ls $destdir/data/${name_dir}_TEI.xml"
    assertTrue "Expected manifest in $destdir" "[ -f $destdir/manifest-sha1.txt ]"
    assertFalse "Should not find $destdir/openn_metadata.xml" "[ -f $destdir/openn_metadata.xml ]"
}

testLewis_e_003() {
    loadDb
    name_dir=FLPLewisE003
    source_dir=${TEST_STAGING_DIR}/$name_dir
    template_dir=${TEST_DATA_DIR}/bibliophilly/$name_dir
    cp -r $template_dir $source_dir
    create_dummy_files $source_dir $LEWIS_E_003_FILES

    output=`op-prep flp-bphil $source_dir`
    status=$?
    if [ "$status" != 0 ]; then echo "$output"; fi

    assertEquals 0 "$status"
    destdir=`get_staging_destination flp $source_dir`
    # save_and_open "$destdir/data/${name_dir}_TEI.xml"
    assertTrue "Expected destination dir $destdir" "[ -d $destdir ]"
    assertTrue "Expected TEI file in $destdir/data; found: `ls $destdir/data 2>/dev/null`" "ls $destdir/data/${name_dir}_TEI.xml"
    assertTrue "Expected manifest in $destdir" "[ -f $destdir/manifest-sha1.txt ]"
    assertFalse "Should not find $destdir/openn_metadata.xml" "[ -f $destdir/openn_metadata.xml ]"
}

testLewis_e_005() {
    loadDb
    name_dir=FLPLewisE005
    source_dir=${TEST_STAGING_DIR}/$name_dir
    template_dir=${TEST_DATA_DIR}/bibliophilly/$name_dir
    cp -r $template_dir $source_dir
    create_dummy_files $source_dir $LEWIS_E_005_FILES

    output=`op-prep flp-bphil $source_dir`
    status=$?
    if [ "$status" != 0 ]; then echo "$output"; fi

    assertEquals 0 "$status"
    destdir=`get_staging_destination flp $source_dir`
    # save_and_open "$destdir/data/${name_dir}_TEI.xml"
    assertTrue "Expected destination dir $destdir" "[ -d $destdir ]"
    assertTrue "Expected TEI file in $destdir/data; found: `ls $destdir/data 2>/dev/null`" "ls $destdir/data/${name_dir}_TEI.xml"
    assertTrue "Expected manifest in $destdir" "[ -f $destdir/manifest-sha1.txt ]"
    assertFalse "Should not find $destdir/openn_metadata.xml" "[ -f $destdir/openn_metadata.xml ]"
}

testLewis_e_009() {
    loadDb
    name_dir=FLPLewisE009
    source_dir=${TEST_STAGING_DIR}/$name_dir
    template_dir=${TEST_DATA_DIR}/bibliophilly/$name_dir
    cp -r $template_dir $source_dir
    create_dummy_files $source_dir $LEWIS_E_009_FILES

    output=`op-prep flp-bphil $source_dir`
    status=$?
    if [ "$status" != 0 ]; then echo "$output"; fi

    assertEquals 0 "$status"
    destdir=`get_staging_destination flp $source_dir`
    # save_and_open "$destdir/data/${name_dir}_TEI.xml"
    assertTrue "Expected destination dir $destdir" "[ -d $destdir ]"
    assertTrue "Expected TEI file in $destdir/data; found: `ls $destdir/data 2>/dev/null`" "ls $destdir/data/${name_dir}_TEI.xml"
    assertTrue "Expected manifest in $destdir" "[ -f $destdir/manifest-sha1.txt ]"
    assertFalse "Should not find $destdir/openn_metadata.xml" "[ -f $destdir/openn_metadata.xml ]"
}

testLewis_e_049() {
    loadDb
    name_dir=FLPLewisE049
    source_dir=${TEST_STAGING_DIR}/$name_dir
    template_dir=${TEST_DATA_DIR}/bibliophilly/$name_dir
    cp -r $template_dir $source_dir
    create_dummy_files $source_dir $LEWIS_E_049_FILES

    output=`op-prep flp-bphil $source_dir`
    status=$?
    if [ "$status" != 0 ]; then echo "$output"; fi

    assertEquals 0 "$status"
    destdir=`get_staging_destination flp $source_dir`
    # save_and_open "$destdir/data/${name_dir}_TEI.xml"
    assertTrue "Expected destination dir $destdir" "[ -d $destdir ]"
    assertTrue "Expected TEI file in $destdir/data; found: `ls $destdir/data 2>/dev/null`" "ls $destdir/data/${name_dir}_TEI.xml"
    assertTrue "Expected manifest in $destdir" "[ -f $destdir/manifest-sha1.txt ]"
    assertFalse "Should not find $destdir/openn_metadata.xml" "[ -f $destdir/openn_metadata.xml ]"
}

# Run shunit
. $shunit
