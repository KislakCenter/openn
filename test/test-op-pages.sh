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
#     suite_addTest testCuratedCollectionTOCOneCollection
#     # suite_addTest testCuratedCollectionTOCOneEmptyCollection
#     # suite_addTest testCuratedCollectionTOCNoDocsOnline
#     # suite_addTest testCuratedCollectionTOCAllCollections
#     # suite_addTest testHtmlTocCuratedFile
#     # suite_addTest testHtmlTocCuratedFileNoDocsOnline
#     # suite_addTest testHtmlTocCuratedFileNoDocs
#     # suite_addTest testHtmlTocCuratedFileBadCollection
#     # suite_addTest testHtmlTocAllCuratedCollections
#     # suite_addTest testHtmlTocCuratedCollectionCSVOnly
#     # suite_addTest testCuratedCollectionsHTML
#     # suite_addTest testDocumentNoTEI
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

setAllDocsOnLine() {
    mysql -u openn openn_test -e "update openn_document set is_online = 1"
}

setAllDocsOffLine() {
    mysql -u openn openn_test -e "update openn_document set is_online = 0"
}

# Usage:
#
#       addADocToCuratedCollection COLL_TAG
addADocToCuratedCollection() {
    adcc_coll_tag=$1
    adcc_doc_id=`get_a_docid`
    # [[ $adcc_doc_id ]] || adcc_doc_id=`get_a_docid`
    add_curated_membership $adcc_coll_tag $adcc_doc_id
}

testRun() {
    # make sure there's at least one curated collection
    setAllDocsOnLine
    addADocToCuratedCollection bibliophilly

    # RUN IT
    output=`op-pages --verbose --show-options`
    status=$?
    if [ $status != 0 ]; then echo "$output"; fi

    assertEquals 0 $status
    assertMatch "$output" "Creating page"
    assertMatch "$output" "Creating TOC"
    assertMatch "$output" "Creating .*Repositories"
    assertMatch "$output" "Skipping"
    assertMatch "$output" "curated collection has no documents:.*pacscl-diaries"
    assertMatch "$output" "Wrote curated collection HTML table of contents.*bibliophilly_contents\.html"
    assertMatch "$output" "Skipping curated collection HTML table of contents.*thai_contents\.html"
    assertMatch "$output" "Wrote curated collection table of contents CSV file:.*bibliophilly_contents\.csv"
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
    output=`op-pages --browse --show-options 2>&1`
    status=$?
    if [ $status != 0 ]; then echo "$output"; fi

    assertEquals 0 $status
    assertMatch "$output" "Creating page"
}

# test browse
testBrowseShortOpt() {
    output=`op-pages -b --show-options 2>&1`
    status=$?
    if [ $status != 0 ]; then echo "$output"; fi

    assertEquals 0 $status
    assertMatch "$output" "Creating page"
}

# test toc
testToc() {
    stagePages

    output=`op-pages --verbose --toc --show-options`
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
    output=`op-pages --readme-file 01_ReadMe.html -v --show-options 2>&1`
    status=$?
    if [ $status == 0 ]; then echo "$output"; fi

    assertNotEquals 0 $status
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

    output=`op-pages --verbose --document $doc_id --show-options`
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

testDocumentNoTEI() {
    doc_id=`mysql -B -u openn openn_test --disable-column-names -e "select max(id) from openn_document where repository_id = 1"`
    # mark the document online to force page generation
    mysql -B -u openn openn_test -e "update openn_document set is_online = 1 where id = $doc_id"
    # clear the TEI content
    mysql -B -u openn openn_test -e "update openn_document set tei_xml = null where id = $doc_id"

    output=`op-pages --document=$doc_id --show-options 2>&1`
    status=$?
    if [ $status == 0 ]; then echo "$output"; fi

    assertNotEquals 0 $status
    assertMatch "$output" "Error processing document with ID $doc_id"
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
    setAllDocsOnLine

    output=`op-pages --csv-toc-repository=ljs --show-options`
    status=$?
    if [ $status != 0 ]; then echo "$output"; fi
    # cat ${STAGED_PAGES}/site/Data/0002_contents.csv

    assertEquals 0 $status
    assertMatch "$output" "Wrote table of contents CSV file:.*0001_contents\.csv"
}

testAllCSVTOCs() {
    stagePages
    setAllDocsOnLine

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
    setAllDocsOnLine

    output=`op-pages --csv-toc-curated=bibliophilly --show-options`
    status=$?
    # cat ${STAGED_PAGES}/site/Data/bibliophilly_contents.csv
    if [ $status != 0 ]; then echo "$output"; fi

    assertEquals 0 $status
    assertMatch "$output" "CSV TOC not makeable; curated collection has no documents"
}

testCuratedCollectionTOCNoDocsOnline() {
    stagePages
    setAllDocsOffLine
    addADocToCuratedCollection bibliophilly

    output=`op-pages --csv-toc-curated=bibliophilly --show-options`
    status=$?
    if [ $status != 0 ]; then echo "$output"; fi

    assertEquals 0 $status
    assertMatch "$output" "CSV TOC not makeable; curated collection has no documents online"
}

testCuratedCollectionTOCOneCollection() {
    stagePages
    setAllDocsOnLine
    addADocToCuratedCollection bibliophilly

    output=`op-pages --csv-toc-curated=bibliophilly --show-options`
    status=$?
    if [ $status != 0 ]; then echo "$output"; fi

    assertEquals 0 $status
    assertMatch "$output" "Wrote curated collection table of contents CSV file:.*bibliophilly_contents\.csv"
}

testCuratedCollectionTOCAllCollections() {
    stagePages
    setAllDocsOnLine
    addADocToCuratedCollection bibliophilly
    addADocToCuratedCollection pacscl-diaries

    output=`op-pages --csv-toc-all-curated --show-options`
    status=$?
    if [ $status != 0 ]; then echo "$output"; fi

    assertEquals 0 $status
    assertMatch "$output" "Wrote curated collection table of contents CSV file:.*bibliophilly_contents\.csv"
    assertMatch "$output" "Wrote curated collection table of contents CSV file:.*pacscl-diaries_contents\.csv"
}

testHtmlTocCuratedFile() {
    stagePages
    setAllDocsOnLine
    addADocToCuratedCollection bibliophilly

    output=`op-pages -v --toc-curated=bibliophilly --show-options`
    output=$output`op-pages -v --toc-curated=bibliophilly`
    # mysql -u $OPENN_DB_USER $OPENN_DB_NAME -e "select * from openn_sitefile"
    status=$?
    if [ $status != 0 ]; then echo "$output"; fi
    # echo "$output"

    assertEquals 0 $status
    assertMatch "$output" "Wrote curated collection HTML table of contents.*bibliophilly_contents\.html"
}

testHtmlTocCuratedFileNoDocs() {
    stagePages
    setAllDocsOnLine
    # don't add any docs

    output=`op-pages --toc-curated=bibliophilly --show-options`
    status=$?
    if [ $status != 0 ]; then echo "$output"; fi

    assertEquals 0 $status
    assertMatch "$output" "curated collection has no documents:.*bibliophilly"
    assertMatch "$output" "Skipping curated collection HTML table of contents.*bibliophilly_contents\.html"
}

testHtmlTocCuratedFileNoDocsOnline() {
    stagePages
    setAllDocsOffLine
    addADocToCuratedCollection bibliophilly

    output=`op-pages --toc-curated=bibliophilly --show-options`
    status=$?
    if [ $status != 0 ]; then echo "$output"; fi

    assertEquals 0 $status
    assertMatch "$output" "curated collection has no documents online:.*bibliophilly"
    assertMatch "$output" "Skipping curated collection HTML table of contents.*bibliophilly_contents\.html"
}

testHtmlTocCuratedFileBadCollection() {
    stagePages
    setAllDocsOffLine

    output=`op-pages --toc-curated=notacollection --show-options`
    status=$?
    if [ $status != 4 ]; then echo "$output"; fi

    assertEquals 4 $status
    assertMatch "$output" "ERROR.*Unknown curated collection"
}

testHtmlTocCuratedCollectionCSVOnly() {
    stagePages
    setAllDocsOnLine
    addADocToCuratedCollection thai

    output=`op-pages --toc-curated=thai --show-options`
    status=$?
    if [ $status != 0 ]; then echo "$output"; fi
    assertEquals 0 $status

    assertMatch "$output" "curated collection is CSV-only.*thai"
    assertMatch "$output" "Skipping curated collection HTML table of contents.*thai_contents\.html"
}

testHtmlTocAllCuratedCollections() {
    stagePages
    setAllDocsOnLine
    addADocToCuratedCollection bibliophilly

    output=`op-pages --toc-all-curated --show-options`
    status=$?
    if [ $status != 0 ]; then echo "$output"; fi
    assertEquals 0 $status

    assertMatch "$output" "Wrote curated collection HTML table of contents.*bibliophilly_contents\.html"
    assertMatch "$output" "Skipping curated collection HTML table of contents.*pacscl-diaries_contents\.html"
}

testCuratedCollectionsHTML() {
    stagePages
    setAllDocsOnLine
    addADocToCuratedCollection bibliophilly

    output=`op-pages --curated-colls --show-options`
    status=$?
    if [ $status != 0 ]; then echo "$output"; fi

    assertEquals 0 $status
    assertMatch "$output" "Creating list of curated collections"
}

# Run shunit
. $shunit
