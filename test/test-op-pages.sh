#!/usr/bin/env sh

THIS_DIR=`dirname $0`
source $THIS_DIR/shunit_helper

TEMPLATE_PAGES=$TEST_DATA_DIR/openn_pages
STAGED_PAGES=$TEST_STAGING_DIR/openn

# suite() {
#     # suite_addTest testRun
#     # suite_addTest testDryRun
#     # suite_addTest testDryRunShortOpt
#     # suite_addTest testForce
#     # suite_addTest testForceShortOpt
#     # suite_addTest testBrowse
#     # suite_addTest testBrowseShortOpt
#     # suite_addTest testToc
#     # suite_addTest testTocShortOpt
#     # suite_addTest testReadMe
#     # suite_addTest testReadMeShortOpt
#     # suite_addTest testReadMeFile
#     # suite_addTest testReadMeFileShortOpt
#     # suite_addTest testReadMeFileFailure
#     # suite_addTest testTocFile
#     # suite_addTest testTocFileShortOpt
#     # suite_addTest testRepositories
#     # suite_addTest testRepositoriesShortOpt
#     # suite_addTest testDocument
#     # suite_addTest testDocumentShortOpt
#     # suite_addTest testNoDocumentRepository
#     # suite_addTest testNoDocumentTocFile
#     # suite_addTest testCollectionsCSV
#     # suite_addTest testCSVTOCRepository
#     # suite_addTest testAllCSVTOCs
#     # suite_addTest testCuratedCollectionTOCOneCollection
#     suite_addTest testCuratedCollectionTOCOneEmptyCollection
#     # suite_addTest testCuratedCollectionTOCAllCollections
# }

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
    assertMatch "$output" "Creating .*Repositories"
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

# test dry run
testDryRunShortOpt() {
    output=`op-pages -n --show-options`
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

# test force
testForceShortOpt() {
    stagePages
    output=`op-pages -f --show-options`
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
    output=`op-pages --browse --show-options 2>&1`
    status=$?
    if [ $status != 0 ]; then echo "$output"; fi
    assertEquals 0 $status
    assertMatch "$output" "Creating page"
}

# test browse
testBrowseShortOpt() {
    # TOOD tests is incorrect; change --dry-run to --browse
    output=`op-pages -b --show-options 2>&1`
    status=$?
    if [ $status != 0 ]; then echo "$output"; fi
    assertEquals 0 $status
    assertMatch "$output" "Creating page"
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

# test TOC for repository
testNoDocumentTocFile() {
    stagePages
    # delete all TOCs to force TOC generation
    find $STAGED_PAGES/site/Repositories -name \*.html -delete
    output=`op-pages --toc-repository tdw --show-options`
    status=$?
    if [ $status != 0 ]; then echo "$output"; fi
    assertEquals 0 $status
    assertMatch "$output" "Creating TOC.*tdw"
}

# test toc
testTocShortOpt() {
    stagePages
    output=`op-pages -t --show-options`
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

# test readme
testReadMeShortOpt() {
    # stagePages
    output=`op-pages -m --show-options`
    status=$?
    if [ $status != 0 ]; then echo "$output"; fi
    assertEquals 0 $status
    assertMatch "$output" "Creating page.*ReadMe"
    assertNotMatch "$output" "Creating page.*ljs454.html"
    assertNotMatch "$output" "Creating TOC"
}

# test readme-file
testReadMeFile() {
    output=`op-pages --readme-file ReadMe.html --show-options`
    status=$?
    if [ $status != 0 ]; then echo "$output"; fi
    assertEquals 0 $status
    assertMatch "$output" "Creating page.*ReadMe"
}

# test readme-file
testReadMeFileShortOpt() {
    output=`op-pages -M ReadMe.html --show-options`
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
    assertMatch "$output" "Unknown readme file"
}

# test TOC for repository
testTocFile() {
    stagePages
    # delete all TOCs to force TOC generation
    find $STAGED_PAGES/site/Repositories -name \*.html -delete
    output=`op-pages --toc-repository ljs --show-options`
    status=$?
    if [ $status != 0 ]; then echo "$output"; fi
    assertEquals 0 $status
    assertMatch "$output" "Creating TOC.*ljs"
}

# test TOC for repository
testTocFileShortOpt() {
    stagePages
    # delete all TOCs to force TOC generation
    find $STAGED_PAGES/site/Repositories -name \*.html -delete
    output=`op-pages -T ljs --show-options`
    status=$?
    if [ $status != 0 ]; then echo "$output"; fi
    assertEquals 0 $status
    assertMatch "$output" "Creating TOC.*ljs"
}

# test repositories
testRepositories() {
    stagePages
    # delete all TOCs to force TOC generation
    find $STAGED_PAGES/site/Repositories -name \*.html -delete
    output=`op-pages --repositories --show-options 2>&1`
    status=$?
    if [ $status != 0 ]; then echo "$output"; fi
    assertEquals 0 $status
    assertMatch "$output" "Creating.*Repositories"
}

# test no_document repository
testNoDocumentRepository() {
    stagePages
    # delete all TOCs to force TOC generation
    find $STAGED_PAGES/site/Repositories -name \*.html -delete
    output=`op-pages --repositories --show-options 2>&1`
    status=$?
    if [ $status != 0 ]; then echo "$output"; fi
    assertEquals 0 $status
    assertMatch "$output" "tdw.*repository is live and is marked no_document"
}

# test repositories with short option
testRepositoriesShortOpt() {
    stagePages
    # delete all TOCs to force TOC generation
    find $STAGED_PAGES/site/Repositories -name \*.html -delete
    output=`op-pages -r --show-options 2>&1`
    status=$?
    if [ $status != 0 ]; then echo "$output"; fi
    assertEquals 0 $status
    assertMatch "$output" "Creating.*Repositories"
}

# test document
testDocument() {
    doc_id=`mysql -B -u openn openn_test --disable-column-names -e "select max(id) from openn_document where repository_id = 1"`
    # mark the document online to force page generation
    mysql -B -u openn openn_test -e "update openn_document set is_online = 1 where id = $doc_id"
    output=`op-pages --document $doc_id --show-options`
    status=$?
    if [ $status != 0 ]; then echo "$output"; fi
    assertEquals 0 $status
    assertMatch "$output" "Creating page"
}

# test document
testDocumentShortOpt() {
    doc_id=`mysql -B -u openn openn_test --disable-column-names -e "select max(id) from openn_document where repository_id = 1"`
    # mark the document online to force page generation
    mysql -B -u openn openn_test -e "update openn_document set is_online = 1 where id = $doc_id"
    output=`op-pages -B $doc_id --show-options`
    status=$?
    if [ $status != 0 ]; then echo "$output"; fi
    assertEquals 0 $status
    assertMatch "$output" "Creating page"
}

testCollectionsCSV() {
    stagePages
    output=`op-pages --collections-csv --show-options`
    status=$?
    # cat ${STAGED_PAGES}/site/Data/collections.csv
    if [ $status != 0 ]; then echo "$output"; fi
    assertEquals 0 $status
    assertMatch "$output" "Wrote repositories CSV file:"
}

testCSVTOCRepository() {
    stagePages
    # make sure documents are marked online
    mysql -u openn openn_test -e "update openn_document set is_online = 1"
    output=`op-pages --csv-toc-repository=ljs --show-options`
    status=$?
    if [ $status != 0 ]; then echo "$output"; fi
    # cat ${STAGED_PAGES}/site/Data/0002_contents.csv
    assertEquals 0 $status
    assertMatch "$output" "Wrote table of contents CSV file:.*0001_contents\.csv"
}

testAllCSVTOCs() {
    stagePages
    # make sure documents are marked online
    mysql -u openn openn_test -e "update openn_document set is_online = 1"
    output=`op-pages --csv-toc --show-options`
    status=$?
    if [ $status != 0 ]; then echo "$output"; fi
    assertEquals 0 $status
    assertMatch "$output" "Wrote table of contents CSV file:.*0001_contents\.csv"
    assertMatch "$output" "CSV TOC not makeable; no HTML dir found.*/0002/"
    assertMatch "$output" "CSV TOC not makeable; repository has no documents online"
}

testCuratedCollectionTOCOneEmptyCollection() {
    stagePages
    mysql -u openn openn_test -e "update openn_document set is_online = 1"
    output=`op-pages --csv-toc-curated=bibliophilly --show-options`
    status=$?
    # cat ${STAGED_PAGES}/site/Data/bibliophilly_contents.csv
    if [ $status != 0 ]; then echo "$output"; fi
    assertEquals 0 $status
    assertMatch "$output" "CSV TOC not makeable; curated collection has no documents online"
}

testCuratedCollectionTOCOneCollection() {
    stagePages
    mysql -u openn openn_test -e "update openn_document set is_online = 1"
    doc_id=`get_a_live_docid`
    # add_curated_membership CURATED_TAG DOCID
    add_curated_membership bibliophilly $doc_id
    output=`op-pages --csv-toc-curated=bibliophilly --show-options`
    status=$?
    # save_and_open "${STAGED_PAGES}/site/Data/bibliophilly_contents.csv"
    if [ $status != 0 ]; then echo "$output"; fi
    assertEquals 0 $status
    assertMatch "$output" "Wrote curated collection table of contents CSV file:.*bibliophilly_contents\.csv"
}


# TODO: create test for curated collection not live

testCuratedCollectionTOCAllCollections() {
    stagePages
    mysql -u openn openn_test -e "update openn_document set is_online = 1"
    doc_id=`get_a_live_docid`
    # add_curated_membership CURATED_TAG DOCID
    add_curated_membership bibliophilly $doc_id
    add_curated_membership pacscl-diaries $doc_id
    output=`op-pages --csv-toc-all-curated --show-options`
    status=$?
    # save_and_open "${STAGED_PAGES}/site/Data/bibliophilly_contents.csv"
    # save_and_open "${STAGED_PAGES}/site/Data/pacscl-diaries_contents.csv"
    if [ $status != 0 ]; then echo "$output"; fi
    assertEquals 0 $status
    assertMatch "$output" "Wrote curated collection table of contents CSV file:.*bibliophilly_contents\.csv"
    assertMatch "$output" "Wrote curated collection table of contents CSV file:.*pacscl-diaries_contents\.csv"
}

# Run shunit
. $shunit
