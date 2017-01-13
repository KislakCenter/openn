#!/usr/bin/env sh

THIS_DIR=`dirname $0`
source $THIS_DIR/shunit_helper

# suite() {
#     # suite_addTest testAddDoc
#     # suite_addTest testAddDocAmbiguousDocument
#     # suite_addTest testAddDocAmbiguousDocumentWithRepository
#     # suite_addTest testAddDocByDocumentId
#     # suite_addTest testAddDocBadDocumentBaseDir
#     # suite_addTest testAddDocBadDocumentId
#     # suite_addTest testAddDocBadCuratedTag
#     # suite_addTest testRmDocByBaseDir
#     # suite_addTest testRmDocByID
#     # suite_addTest testRmDocAmbiguousDocument
#     # suite_addTest testRmDocAmbiguousDocumentWithRepository
#     # suite_addTest testRmDocByDocumentId
#     # suite_addTest testRmDocBadDocumentBaseDir
#     # suite_addTest testRmDocBadDocumentId
#     # suite_addTest testRmDocBadCuratedTag
#     # suite_addTest testBulkAddValidDocIdCSV
#     # suite_addTest testBulkAddValidDocBasedirCSV
#     # suite_addTest testBulkAddByDocumentIDWithErrors
#     # suite_addTest testBulkAddByDocumentBaseDirWithErrors
#     # suite_addTest testBulkRmValidDocIdCSV
#     # suite_addTest testBulkRmValidDocBasedirCSV
#     # suite_addTest testBulkRmByDocumentIDWithErrors
#     # suite_addTest testRmDocByIdNotInCuratedCollection
#     suite_addTest testBulkRmByDocumentBaseDirWithErrors
# }

setUp() {
    # make sure the database is empty
    clear_tables
    loadDb
}

tearDown() {
    clear_tables
    rm -rf $TEMP_FILE*
}

testAddDoc() {
    insert_document mscodex123 pennmss
    output=`op-curt add-doc bibliophilly mscodex123`

    status=$?
    if [ $status != 0 ]
    then
        echo "$output"
    fi
    assertEquals 0 $status
    assertMatch "$output" 'Added'
}

testAddDocAmbiguousDocument() {
    insert_document mscodex123 pennmss
    insert_document mscodex123 ljs
    output=`op-curt add-doc bibliophilly mscodex123`
    status=$?
    if [ $status != 1 ]
    then
        echo "$output"
    fi
    assertEquals 1 $status
    assertMatch "$output" "Ambiguous"
}

testAddDocAmbiguousDocumentWithRepository() {
    insert_document mscodex123 pennmss
    insert_document mscodex123 ljs
    output=`op-curt add-doc --repository ljs bibliophilly mscodex123`

    status=$?
    if [ $status != 0 ]
    then
        echo "$output"
    fi
    assertEquals 0 $status
    assertMatch "$output" 'Added'
}

testAddDocByDocumentId() {
    insert_document mscodex123 pennmss
    doc_id=`get_document_id mscodex123 pennmss`
    insert_document mscodex123 ljs

    output=`op-curt add-doc bibliophilly $doc_id`

    status=$?
    if [ $status != 0 ]
    then
        echo "$output"
    fi
    assertEquals 0 $status
    assertMatch "$output" 'Added'
}

testAddDocBadDocumentBaseDir() {
    insert_document mscodex123 pennmss
    # use the wrong document tag
    output=`op-curt add-doc bibliophilly mscodex124`

    status=$?

    if [ $status = 0 ]
    then
        echo "$output"
    fi
    assertNotEquals 0 $status
    assertMatch "$output" 'Unknown document'
}

testAddDocBadDocumentId() {
    insert_document mscodex123 pennmss
    doc_id=`get_document_id mscodex123 pennmss`
    doc_id=$(( doc_id + 1 ))
    # use the wrong document tag
    output=`op-curt add-doc bibliophilly $doc_id`

    status=$?

    if [ $status = 0 ]
    then
        echo "$output"
    fi
    assertNotEquals 0 $status
    assertMatch "$output" 'Unknown document'
}

testAddDocBadCuratedTag() {
    insert_document mscodex123 pennmss
    # use a bad curated collection tag
    output=`op-curt add-doc xxx mscodex123`

    status=$?
    if [ $status = 0 ]
    then
        echo "$output"
    fi
    assertNotEquals 0 $status
    assertMatch "$output" 'Unknown curated collection'
}

testRmDocByBaseDir() {
    insert_document mscodex123 pennmss
    # get_document_id mscodex123 pennmss
    doc_id=`get_document_id mscodex123 pennmss`
    add_curated_membership bibliophilly $doc_id
    output=`op-curt rm-doc bibliophilly mscodex123`

    status=$?
    if [ $status != 0 ];
    then
        echo "$output"
    fi

    assertEquals 0 $status
    assertMatch "$output" 'Removed'
}

testRmDocByID() {
    insert_document mscodex123 pennmss
    # get_document_id mscodex123 pennmss
    doc_id=`get_document_id mscodex123 pennmss`
    add_curated_membership bibliophilly $doc_id
    output=`op-curt rm-doc bibliophilly $doc_id`

    status=$?
    if [ $status != 0 ];
    then
        echo "$output"
    fi

    assertEquals 0 $status
    assertMatch "$output" 'Removed'
}

testRmDocAmbiguousDocument() {
    # Set up ambiguous documents and add one to a repository.
    insert_document mscodex123 pennmss
    insert_document mscodex123 ljs
    doc_id=`get_document_id mscodex123 ljs`
    add_curated_membership bibliophilly $doc_id

    output=`op-curt rm-doc bibliophilly mscodex123`
    status=$?
    if [ $status != 1 ]
    then
        echo "$output"
    fi
    assertEquals 1 $status
    assertMatch "$output" "Ambiguous"
}

testRmDocAmbiguousDocumentWithRepository() {
    # Set up ambiguous documents and add one to a repository.
    insert_document mscodex123 pennmss
    insert_document mscodex123 ljs
    doc_id=`get_document_id mscodex123 ljs`
    add_curated_membership bibliophilly $doc_id

    output=`op-curt rm-doc --repository ljs bibliophilly mscodex123`

    status=$?
    if [ $status != 0 ]
    then
        echo "$output"
    fi
    assertEquals 0 $status
    assertMatch "$output" 'Removed'
}

testRmDocByDocumentId() {
    insert_document mscodex123 pennmss
    doc_id=`get_document_id mscodex123 pennmss`
    add_curated_membership bibliophilly $doc_id

    output=`op-curt rm-doc bibliophilly $doc_id`

    status=$?
    if [ $status != 0 ]
    then
        echo "$output"
    fi
    assertEquals 0 $status
    assertMatch "$output" 'Removed'
}

testRmDocBadDocumentBaseDir() {
    insert_document mscodex123 pennmss
    doc_id=`get_document_id mscodex123 pennmss`
    add_curated_membership bibliophilly $doc_id

    # use the wrong document base_dir
    output=`op-curt rm-doc bibliophilly mscodex124`

    status=$?
    if [ $status = 0 ]
    then
        echo "$output"
    fi

    assertNotEquals 0 $status
    assertMatch "$output" 'Unknown document'
}

testRmDocBadDocumentId() {
    insert_document mscodex123 pennmss
    doc_id=`get_document_id mscodex123 pennmss`
    add_curated_membership bibliophilly $doc_id

    # use the wrong document ID
    doc_id=$(( doc_id + 1 ))
    output=`op-curt rm-doc bibliophilly $doc_id`

    status=$?

    if [ $status = 0 ]
    then
        echo "$output"
    fi
    assertNotEquals 0 $status
    assertMatch "$output" 'Unknown document'
}

testRmDocBadCuratedTag() {
    insert_document mscodex123 pennmss
    doc_id=`get_document_id mscodex123 pennmss`
    add_curated_membership bibliophilly $doc_id

    # use a bad curated tag
    output=`op-curt rm-doc xxx mscodex123`

    status=$?
    if [ $status = 0 ]
    then
        echo "$output"
    fi
    assertNotEquals 0 $status
    assertMatch "$output" 'Unknown curated collection'
}

testRmDocByIdNotInCuratedCollection() {
    insert_document mscodex123 pennmss
    doc_id=`get_document_id mscodex123 pennmss`

    # try to remove a document not assigned to a curated collection; both
    # curated collection and doc_id are valid
    output=`op-curt rm-doc bibliophilly $doc_id`

    status=$?
    if [ $status = 0 ]
    then
        echo "$output"
    fi
    assertNotEquals 0 $status
    assertMatch "$output" 'Document not in curated collection'
}

testBulkAddValidDocIdCSV() {
    insert_document mscodex123 pennmss
    insert_document mscodex124 pennmss
    id1=`get_document_id mscodex123 pennmss`
    id2=`get_document_id mscodex124 pennmss`
    csvfile=${TEMP_FILE}.1
    echo 'curated_collection_tag,document_id' > $csvfile
    echo "bibliophilly,${id1}" >> $csvfile
    echo "bibliophilly,${id2}" >> $csvfile

    output=`op-curt bulk-add $csvfile`

    status=$?
    if [ $status != 0 ]
    then
        echo "$output"
    fi
    assertEquals 0 $status
    assertMatch "$output" 'Added document to curated collection'
    assertNotMatch "$output" 'Error adding document'
}

testBulkAddValidDocBasedirCSV() {
    insert_document mscodex123 pennmss
    insert_document mscodex124 pennmss
    csvfile=${TEMP_FILE}.1
    echo 'curated_collection_tag,document_base_dir,repository_tag' > $csvfile
    echo "bibliophilly,mscodex123,pennmss" >> $csvfile
    echo "bibliophilly,mscodex124,pennmss" >> $csvfile

    output=`op-curt bulk-add $csvfile`

    status=$?
    if [ $status != 0 ]
    then
        echo "$output"
    fi
    assertEquals 0 $status
    assertMatch "$output" 'Added document to curated collection'
    assertNotMatch "$output" 'Error adding document'
}

testBulkAddByDocumentIDWithErrors() {
    insert_document mscodex123 pennmss
    insert_document mscodex124 pennmss
    id1=`get_document_id mscodex123 pennmss`
    id2=`get_document_id mscodex124 pennmss`
    id3=$((id2 + 1))
    csvfile=${TEMP_FILE}.3
    echo 'curated_collection_tag,document_id' > $csvfile

    # 2 good lines
    echo "bibliophilly,${id1}" >> $csvfile
    echo "bibliophilly,${id2}" >> $csvfile

    # 3 ERROR lines
    # insert non-existent id
    echo "bibliophilly,${id3}" >> $csvfile
    # insert bad curated collection
    echo "FALSE_CURATED,${id2}" >> $csvfile
    # insert duplicate
    echo "bibliophilly,${id2}" >> $csvfile

    output=`op-curt bulk-add $csvfile`
    status=$?
    if [ $status != 0 ]
    then
        echo "$output"
    fi
    assertEquals 0 $status
    assertMatch "$output" 'Added document to curated collection'
    assertNumberOfMatchingLines "$output" 'Added document to curated collection' 2
    assertNumberOfMatchingLines "$output" 'Unknown document' 1
    assertNumberOfMatchingLines "$output" 'Unknown curated collection' 1
    assertNumberOfMatchingLines "$output" 'Membership already exists' 1
}

testBulkAddByDocumentBaseDirWithErrors() {
    insert_document mscodex123 pennmss
    insert_document mscodex124 pennmss

    csvfile=${TEMP_FILE}.1
    echo 'curated_collection_tag,document_base_dir,repository_tag' > $csvfile

    # Insert 2 good lines
    echo "bibliophilly,mscodex123,pennmss" >> $csvfile
    echo "bibliophilly,mscodex124,pennmss" >> $csvfile

    # ERROR lines
    # insert bad base_dir
    echo "bibliophilly,mscodex125,pennmss" >> $csvfile
    # insert duplicate
    echo "bibliophilly,mscodex124,pennmss" >> $csvfile

    output=`op-curt bulk-add $csvfile`
    status=$?
    if [ $status != 0 ]
    then
        echo "$output"
    fi
    assertEquals 0 $status
    assertMatch "$output" 'Added document to curated collection'
    assertNumberOfMatchingLines "$output" 'Added document to curated collection' 2
    assertNumberOfMatchingLines "$output" 'Unknown document' 1
    assertNumberOfMatchingLines "$output" 'Membership already exists' 1
}

testBulkRmValidDocIdCSV() {
    insert_document mscodex123 pennmss
    insert_document mscodex124 pennmss
    id1=`get_document_id mscodex123 pennmss`
    id2=`get_document_id mscodex124 pennmss`
    add_curated_membership bibliophilly $id1
    add_curated_membership bibliophilly $id2

    csvfile=${TEMP_FILE}.1
    echo 'curated_collection_tag,document_id' > $csvfile
    echo "bibliophilly,${id1}" >> $csvfile
    echo "bibliophilly,${id2}" >> $csvfile

    output=`op-curt bulk-rm $csvfile`

    status=$?
    if [ $status != 0 ]
    then
        echo "$output"
    fi
    assertEquals 0 $status
    assertNumberOfMatchingLines "$output" 'Removed document .*from curated collection' 2
    assertNotMatch "$output" 'ERROR'
}

testBulkRmValidDocBasedirCSV() {
    insert_document mscodex123 pennmss
    insert_document mscodex124 pennmss
    id1=`get_document_id mscodex123 pennmss`
    id2=`get_document_id mscodex124 pennmss`
    add_curated_membership bibliophilly $id1
    add_curated_membership bibliophilly $id2

    csvfile=${TEMP_FILE}.1
    echo 'curated_collection_tag,document_base_dir,repository_tag' > $csvfile
    echo "bibliophilly,mscodex123,pennmss" >> $csvfile
    echo "bibliophilly,mscodex124,pennmss" >> $csvfile

    output=`op-curt bulk-rm $csvfile`

    status=$?
    if [ $status != 0 ]
    then
        echo "$output"
    fi
    assertEquals 0 $status
    assertNumberOfMatchingLines "$output" 'Removed document .*from curated collection' 2
    assertNotMatch "$output" 'ERROR'
}

testBulkRmByDocumentIDWithErrors() {
    insert_document mscodex123 pennmss
    insert_document mscodex124 pennmss
    id1=`get_document_id mscodex123 pennmss`
    id2=`get_document_id mscodex124 pennmss`
    add_curated_membership bibliophilly $id1
    add_curated_membership bibliophilly $id2


    csvfile=${TEMP_FILE}.3
    echo 'curated_collection_tag,document_id' > $csvfile

    # 2 good lines
    echo "bibliophilly,${id1}" >> $csvfile
    echo "bibliophilly,${id2}" >> $csvfile

    # 3 ERROR lines
    # use non-existent id
    id3=$((id2 + 1)) # <= bad id
    echo "bibliophilly,${id3}" >> $csvfile
    # use non-existent curated collection
    echo "FALSE_CURATED,${id2}" >> $csvfile
    # try to remove document second time;
    # should have error 'Document not in curated collection'
    echo "bibliophilly,${id2}" >> $csvfile

    output=`op-curt bulk-rm $csvfile`
    status=$?
    if [ $status != 0 ]
    then
        echo "$output"
    fi
    assertEquals 0 $status
    assertNumberOfMatchingLines "$output" 'Removed document .*from curated collection' 2
    assertNumberOfMatchingLines "$output" 'Unknown document' 1
    assertNumberOfMatchingLines "$output" 'Unknown curated collection' 1
    assertNumberOfMatchingLines "$output" 'Document not in curated collection' 1
}

testBulkRmByDocumentBaseDirWithErrors() {
    insert_document mscodex123 pennmss
    insert_document mscodex124 pennmss
    id1=`get_document_id mscodex123 pennmss`
    id2=`get_document_id mscodex124 pennmss`
    add_curated_membership bibliophilly $id1
    add_curated_membership bibliophilly $id2

    csvfile=${TEMP_FILE}.1
    echo 'curated_collection_tag,document_base_dir,repository_tag' > $csvfile

    # Insert 2 good lines
    echo "bibliophilly,mscodex123,pennmss" >> $csvfile
    echo "bibliophilly,mscodex124,pennmss" >> $csvfile

    # ERROR lines
    # use non-existent base_dir
    echo "bibliophilly,mscodex125,pennmss" >> $csvfile
    # use non-existent curated collection
    echo "FALSE_CURATED,mscodex124,pennmss" >> $csvfile
    # try to remove document second time;
    # should have error 'Document not in curated collection'
    echo "bibliophilly,mscodex124,pennmss" >> $csvfile

    output=`op-curt bulk-rm $csvfile`
    status=$?
    if [ $status != 0 ]
    then
        echo "$output"
    fi
    assertEquals 0 $status
    assertNumberOfMatchingLines "$output" 'Removed document .*from curated collection' 2
    assertNumberOfMatchingLines "$output" 'Unknown document' 1
    assertNumberOfMatchingLines "$output" 'Unknown curated collection' 1
    assertNumberOfMatchingLines "$output" 'Document not in curated collection' 1
}

# Run shunit
. $shunit
