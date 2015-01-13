#!/usr/bin/env sh

THIS_DIR=`dirname $0`
source $THIS_DIR/shunit_helper

TEMPLATE_PAGES=$TEST_DATA_DIR/openn_pages
STAGED_PAGES=$TEST_STAGING_DIR/openn

suite() {
    suite_addTest testCollection
}

setUp() {
    if [ ! -d $TEST_STAGING_DIR ]; then
        mkdir $TEST_STAGING_DIR
    fi
    # make sure the database is empty
    clear_tables
    mysql -u $OPENN_DB_USER --default-character-set=utf8 openn_test < $THIS_DIR/fixtures/test.sql
}

tearDown() {
    clear_tables
    rm -rf $TEST_STAGING_DIR/* 2>/dev/null
}

stagePages() {
    # make sure the staged data isn't there
    rm -rf $STAGED_DATA
    cp -r $TEMPLATE_PAGES $STAGED_PAGES
}

testRun() {
    output=`op-pages --show-options`
    status=$?
    if [ $status != 0 ]; then echo "$output"; fi
    assertEquals 0 $status
    assertMatch "$output" "Creating page"
    assertMatch "$output" "Creating TOC"
    assertMatch "$output" "Skipping"
}

# test dry run
testDryRun() {
    output=`op-pages --dry-run --show-options`
    status=$?
    if [ $status != 0 ]; then echo "$output"; fi
    assertEquals 0 $status
    assertMatch "$output" "DRY RUN COMPLETE"
    assertMatch "$output" "Skipping"

}

# test force
testForce() {
    stagePages
    output=`op-pages --force --show-options`
    status=$?
    if [ $status != 0 ]; then echo "$output"; fi
    assertEquals 0 $status
    assertMatch "$output" "Creating page.*ReadMe"
    assertMatch "$output" "Creating page.*ljs454.html"
    assertMatch "$output" "Creating TOC"
    assertMatch "$output" "Skipping"
}

# test browse
testBrowse() {
    # TOOD tests is incorrect; change --dry-run to --browse
    output=`op-pages --dry-run --show-options 2>&1`
    status=$?
    if [ $status != 0 ]; then echo "$output"; fi
    assertEquals 0 $status
    assertMatch "$output" "Creating page"
    assertMatch "$output" "Skipping"
}

# test toc
testToc() {
    stagePages
    output=`op-pages --toc --show-options`
    status=$?
    if [ $status != 0 ]; then echo "$output"; fi
    assertEquals 0 $status
    assertMatch "$output" "Creating TOC"
    assertMatch "$output" "Skipping TOC"
}

# test readme
testReadMe() {
    # stagePages
    output=`op-pages --readme --show-options`
    status=$?
    if [ $status != 0 ]; then echo "$output"; fi
    assertEquals 0 $status
    assertMatch "$output" "Creating page.*ReadMe"
    assertNotMatch "$output" "Creating page.*ljs454.html"
    assertNotMatch "$output" "Creating TOC"
}

# test readme-file
testReadMeFile() {
    output=`op-pages --readme-file 0_ReadMe.html --show-options`
    status=$?
    if [ $status != 0 ]; then echo "$output"; fi
    assertEquals 0 $status
    assertMatch "$output" "Creating page.*ReadMe"
}

# test readme-file failure
testReadMeFileFailure() {
    output=`op-pages --readme-file 01_ReadMe.html --show-options 2>&1`
    status=$?
    if [ $status != 2 ]; then echo "$output"; fi
    assertEquals 2 $status
    assertMatch "$output" "Could not find template.*ReadMe"
}

# test collection
testCollection() {
    stagePages
    # delete all TOCs to force TOC generation
    find $STAGED_PAGES -name TOC_\*.html -delete
    output=`op-pages --collection ljs --show-options`
    status=$?
    if [ $status != 0 ]; then echo "$output"; fi
    assertEquals 0 $status
    assertMatch "$output" "Creating TOC.*LJS"
}

# test document
testDocument() {
    doc_id=`mysql -B -u openn openn_test --disable-column-names -e "select max(id) from openn_document where collection = 'ljs'"`
    # mark the document online to force page generation
    mysql -B -u openn openn_test -e "update openn_document set is_online = 1 where id = $doc_id"
    output=`op-pages --document $doc_id --show-options`
    status=$?
    if [ $status != 0 ]; then echo "$output"; fi
    assertEquals 0 $status
    assertMatch "$output" "Creating page"
}

# Run shunit
. $shunit
