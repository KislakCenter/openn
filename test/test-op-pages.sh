#!/usr/bin/env sh

THIS_DIR=`dirname $0`
source $THIS_DIR/shunit_helper

TEMPLATE_PAGES=$TEST_DATA_DIR/openn_pages
STAGED_PAGES=$TEST_STAGING_DIR/openn

# suite() {
#     suite_addTest testForce
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

stagePages() {
    # make sure the staged data isn't there
    rm -rf $STAGED_DATA
    cp -r $TEMPLATE_PAGES $STAGED_PAGES
}

testRun() {
    mysql -u $OPENN_DB_USER --default-character-set=utf8 openn_test < $THIS_DIR/fixtures/test.sql
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
    mysql -u $OPENN_DB_USER --default-character-set=utf8 openn_test < $THIS_DIR/fixtures/test.sql
    output=`op-pages --dry-run --show-options`
    status=$?
    if [ $status != 0 ]; then echo "$output"; fi
    assertEquals 0 $status
    assertMatch "$output" "DRY RUN COMPLETE"
    assertMatch "$output" "Skipping"

}

# test force
testForce() {
    mysql -u $OPENN_DB_USER --default-character-set=utf8 openn_test < $THIS_DIR/fixtures/test.sql
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
    mysql -u $OPENN_DB_USER --default-character-set=utf8 openn_test < $THIS_DIR/fixtures/test.sql
    output=`op-pages --dry-run --show-options`
    status=$?
    if [ $status != 0 ]; then echo "$output"; fi
    assertEquals 0 $status
    assertMatch "$output" "Creating page"
    assertMatch "$output" "Skipping"
}

# test toc

# test readme

# test readme-file

# test collection

# test document

# Run shunit
. $shunit
