#!/usr/bin/env sh

THIS_DIR=`dirname $0`
source $THIS_DIR/shunit_helper

# suite() {
#     # suite_addTest testAddDoc
#     # suite_addTest testAddDocAmbiguousDocument
#     # suite_addTest testAddDocAmbiguousDocumentWithPrimaryCollection
#     # suite_addTest testAddDocByDocumentId
#     # suite_addTest testAddDocBadDocumentBaseDir
#     # suite_addTest testAddDocBadDocumentId
#     # suite_addTest testAddDocBadProjectTag
#     # suite_addTest testRmDocByBaseDir
#     # suite_addTest testRmDocByID
#     # suite_addTest testRmDocAmbiguousDocument
#     # suite_addTest testRmDocAmbiguousDocumentWithPrimaryCollection
#     # suite_addTest testRmDocByDocumentId
#     # suite_addTest testRmDocBadDocumentBaseDir
#     # suite_addTest testRmDocBadDocumentId
#     # suite_addTest testRmDocBadProjectTag
#     # suite_addTest testBulkAddValidDocIdCSV
#     # suite_addTest testBulkAddValidDocBasedirCSV
#     # suite_addTest testBulkAddByDocumentIDWithErrors
#     # suite_addTest testBulkAddByDocumentBaseDirWithErrors
#     # suite_addTest testBulkRmValidDocIdCSV
#     # suite_addTest testBulkRmValidDocBasedirCSV
#     # suite_addTest testBulkRmByDocumentIDWithErrors
#     # suite_addTest testRmDocByIdNotInProject
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

# Usage: get_collection_id COLL_TAG
#
# Print the ID of the collection with tag COLL_TAG.
get_collection_id() {
    gci_tag=${1?get_collection_id - tag required}
    gci_id=`mysql --batch --skip-column-names -u openn $OPENN_DB_NAME -e "select id from openn_openncollection where tag = '$gci_tag'"`
    [[ -z "$gci_id" ]] && return 1
    echo $gci_id
    return 0
}

# Usage: get_project_id PROJ_TAG
#
# Print the ID of the project with tag PROJ_TAG.
get_project_id() {
    gpi_tag=${1?get_project_id - tag required}
    gpi_id=`mysql --batch --skip-column-names -u openn $OPENN_DB_NAME -e "select id from openn_project where tag = '$gpi_tag'"`
    [[ -z "$gpi_id" ]] && return 1
    echo $gpi_id
    return 0
}

# Usage: get_document_id BASE_DIR COLL_TAG
#
# Print the document ID for the document with base_dir BASE_DIR in the
# collection with tag COLL_TAG.
get_document_id() {
    gdi_base_dir=${1?get_document_id - base_dir required}
    gdi_collection_tag=${2?get_document_id - collection_tag required}

    gdi_coll_id=`get_collection_id $gdi_collection_tag`
    gdi_doc_id=`mysql --batch --skip-column-names -u openn $OPENN_DB_NAME -e "select id from openn_document where base_dir = '$gdi_base_dir' and openn_collection_id = $gdi_coll_id"`

    if [[ "$gdi_doc_id" ]]; then
        echo "$gdi_doc_id"
        return 0
    else
        return 1
    fi
}

# Usage: add_membership PROJECT_TAG DOCID
add_project_membership() {
    am_proj_tag=${1?add_membership - PROJECT_TAG required}
    am_docid=${2?add_membership - DOCID required}

    # echo "=== $am_docid"
    am_proj_id=`get_project_id $am_proj_tag`
    today=`date "+%Y-%m-%d"`
    sql="insert into openn_projectmembership"
    sql="$sql (project_id, document_id, created, updated)"
    sql="$sql values ($am_proj_id, $am_docid, '$today', '$today')"
    mysql -u $OPENN_DB_USER $OPENN_DB_NAME -e "$sql"
}

# Usage: insert_document BASE_DIR COLL_TAG
#
# Insert new document with BASE_DIR, linked to collection with tag COLL_TAG.
insert_document() {
    id_base_dir=${1?insert_document - base_dir required}
    id_collection_tag=${2?insert_document - collection_tag required}
    today=`date "+%Y-%m-%d"`
    collection_id=`get_collection_id $id_collection_tag` || {
        echo  "ERROR: $id_collection_tag not in collections table";
        exit 1; }
    sql="insert into openn_document"
    sql="$sql (openn_collection_id, base_dir, is_online, created, updated)"
    sql="$sql values ($collection_id, '$id_base_dir', 0, '$today', '$today')"
    mysql -u $OPENN_DB_USER $OPENN_DB_NAME -e "$sql"
}

testAddDoc() {
    insert_document mscodex123 pennmss
    output=`op-proj add-doc bibliophilly mscodex123`

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
    output=`op-proj add-doc bibliophilly mscodex123`
    status=$?
    if [ $status != 1 ]
    then
        echo "$output"
    fi
    assertEquals 1 $status
    assertMatch "$output" "Ambiguous"
}

testAddDocAmbiguousDocumentWithPrimaryCollection() {
    insert_document mscodex123 pennmss
    insert_document mscodex123 ljs
    output=`op-proj add-doc --primary-collection ljs bibliophilly mscodex123`

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

    output=`op-proj add-doc bibliophilly $doc_id`

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
    output=`op-proj add-doc bibliophilly mscodex124`

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
    output=`op-proj add-doc bibliophilly $doc_id`

    status=$?

    if [ $status = 0 ]
    then
        echo "$output"
    fi
    assertNotEquals 0 $status
    assertMatch "$output" 'Unknown document'
}

testAddDocBadProjectTag() {
    insert_document mscodex123 pennmss
    # use a bad project tag
    output=`op-proj add-doc xxx mscodex123`

    status=$?
    if [ $status = 0 ]
    then
        echo "$output"
    fi
    assertNotEquals 0 $status
    assertMatch "$output" 'Unknown project'
}

testRmDocByBaseDir() {
    insert_document mscodex123 pennmss
    # get_document_id mscodex123 pennmss
    doc_id=`get_document_id mscodex123 pennmss`
    add_project_membership bibliophilly $doc_id
    output=`op-proj rm-doc bibliophilly mscodex123`

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
    add_project_membership bibliophilly $doc_id
    output=`op-proj rm-doc bibliophilly $doc_id`

    status=$?
    if [ $status != 0 ];
    then
        echo "$output"
    fi

    assertEquals 0 $status
    assertMatch "$output" 'Removed'
}

testRmDocAmbiguousDocument() {
    # Set up ambiguous documents and add one to a collection.
    insert_document mscodex123 pennmss
    insert_document mscodex123 ljs
    doc_id=`get_document_id mscodex123 ljs`
    add_project_membership bibliophilly $doc_id

    output=`op-proj rm-doc bibliophilly mscodex123`
    status=$?
    if [ $status != 1 ]
    then
        echo "$output"
    fi
    assertEquals 1 $status
    assertMatch "$output" "Ambiguous"
}

testRmDocAmbiguousDocumentWithPrimaryCollection() {
    # Set up ambiguous documents and add one to a collection.
    insert_document mscodex123 pennmss
    insert_document mscodex123 ljs
    doc_id=`get_document_id mscodex123 ljs`
    add_project_membership bibliophilly $doc_id

    output=`op-proj rm-doc --primary-collection ljs bibliophilly mscodex123`

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
    add_project_membership bibliophilly $doc_id

    output=`op-proj rm-doc bibliophilly $doc_id`

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
    add_project_membership bibliophilly $doc_id

    # use the wrong document base_dir
    output=`op-proj rm-doc bibliophilly mscodex124`

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
    add_project_membership bibliophilly $doc_id

    # use the wrong document ID
    doc_id=$(( doc_id + 1 ))
    output=`op-proj rm-doc bibliophilly $doc_id`

    status=$?

    if [ $status = 0 ]
    then
        echo "$output"
    fi
    assertNotEquals 0 $status
    assertMatch "$output" 'Unknown document'
}

testRmDocBadProjectTag() {
    insert_document mscodex123 pennmss
    doc_id=`get_document_id mscodex123 pennmss`
    add_project_membership bibliophilly $doc_id

    # use a bad project tag
    output=`op-proj rm-doc xxx mscodex123`

    status=$?
    if [ $status = 0 ]
    then
        echo "$output"
    fi
    assertNotEquals 0 $status
    assertMatch "$output" 'Unknown project'
}

testRmDocByIdNotInProject() {
    insert_document mscodex123 pennmss
    doc_id=`get_document_id mscodex123 pennmss`

    # try to remove a document not assigned to a project; both project and
    # doc_id are valid
    output=`op-proj rm-doc bibliophilly $doc_id`

    status=$?
    if [ $status = 0 ]
    then
        echo "$output"
    fi
    assertNotEquals 0 $status
    assertMatch "$output" 'Document not in project'
}

testBulkAddValidDocIdCSV() {
    insert_document mscodex123 pennmss
    insert_document mscodex124 pennmss
    id1=`get_document_id mscodex123 pennmss`
    id2=`get_document_id mscodex124 pennmss`
    csvfile=${TEMP_FILE}.1
    echo 'project_tag,document_id' > $csvfile
    echo "bibliophilly,${id1}" >> $csvfile
    echo "bibliophilly,${id2}" >> $csvfile

    output=`op-proj bulk-add $csvfile`

    status=$?
    if [ $status != 0 ]
    then
        echo "$output"
    fi
    assertEquals 0 $status
    assertMatch "$output" 'Added document to project'
    assertNotMatch "$output" 'Error adding document'
}

testBulkAddValidDocBasedirCSV() {
    insert_document mscodex123 pennmss
    insert_document mscodex124 pennmss
    csvfile=${TEMP_FILE}.1
    echo 'project_tag,document_base_dir,collection_tag' > $csvfile
    echo "bibliophilly,mscodex123,pennmss" >> $csvfile
    echo "bibliophilly,mscodex124,pennmss" >> $csvfile

    output=`op-proj bulk-add $csvfile`

    status=$?
    if [ $status != 0 ]
    then
        echo "$output"
    fi
    assertEquals 0 $status
    assertMatch "$output" 'Added document to project'
    assertNotMatch "$output" 'Error adding document'
}

testBulkAddByDocumentIDWithErrors() {
    insert_document mscodex123 pennmss
    insert_document mscodex124 pennmss
    id1=`get_document_id mscodex123 pennmss`
    id2=`get_document_id mscodex124 pennmss`
    id3=$((id2 + 1))
    csvfile=${TEMP_FILE}.3
    echo 'project_tag,document_id' > $csvfile

    # 2 good lines
    echo "bibliophilly,${id1}" >> $csvfile
    echo "bibliophilly,${id2}" >> $csvfile

    # 3 ERROR lines
    # insert non-existent id
    echo "bibliophilly,${id3}" >> $csvfile
    # insert bad project
    echo "FALSE_PROJECT,${id2}" >> $csvfile
    # insert duplicate
    echo "bibliophilly,${id2}" >> $csvfile

    output=`op-proj bulk-add $csvfile`
    status=$?
    if [ $status != 0 ]
    then
        echo "$output"
    fi
    assertEquals 0 $status
    assertMatch "$output" 'Added document to project'
    assertNumberOfMatchingLines "$output" 'Added document to project' 2
    assertNumberOfMatchingLines "$output" 'Unknown document' 1
    assertNumberOfMatchingLines "$output" 'Unknown project' 1
    assertNumberOfMatchingLines "$output" 'Membership already exists' 1
}

testBulkAddByDocumentBaseDirWithErrors() {
    insert_document mscodex123 pennmss
    insert_document mscodex124 pennmss

    csvfile=${TEMP_FILE}.1
    echo 'project_tag,document_base_dir,collection_tag' > $csvfile

    # Insert 2 good lines
    echo "bibliophilly,mscodex123,pennmss" >> $csvfile
    echo "bibliophilly,mscodex124,pennmss" >> $csvfile

    # ERROR lines
    # insert bad base_dir
    echo "bibliophilly,mscodex125,pennmss" >> $csvfile
    # insert duplicate
    echo "bibliophilly,mscodex124,pennmss" >> $csvfile

    output=`op-proj bulk-add $csvfile`
    status=$?
    if [ $status != 0 ]
    then
        echo "$output"
    fi
    assertEquals 0 $status
    assertMatch "$output" 'Added document to project'
    assertNumberOfMatchingLines "$output" 'Added document to project' 2
    assertNumberOfMatchingLines "$output" 'Unknown document' 1
    assertNumberOfMatchingLines "$output" 'Membership already exists' 1
}

testBulkRmValidDocIdCSV() {
    insert_document mscodex123 pennmss
    insert_document mscodex124 pennmss
    id1=`get_document_id mscodex123 pennmss`
    id2=`get_document_id mscodex124 pennmss`
    add_project_membership bibliophilly $id1
    add_project_membership bibliophilly $id2

    csvfile=${TEMP_FILE}.1
    echo 'project_tag,document_id' > $csvfile
    echo "bibliophilly,${id1}" >> $csvfile
    echo "bibliophilly,${id2}" >> $csvfile

    output=`op-proj bulk-rm $csvfile`

    status=$?
    if [ $status != 0 ]
    then
        echo "$output"
    fi
    assertEquals 0 $status
    assertNumberOfMatchingLines "$output" 'Removed document .*from project' 2
    assertNotMatch "$output" 'ERROR'
}

testBulkRmValidDocBasedirCSV() {
    insert_document mscodex123 pennmss
    insert_document mscodex124 pennmss
    id1=`get_document_id mscodex123 pennmss`
    id2=`get_document_id mscodex124 pennmss`
    add_project_membership bibliophilly $id1
    add_project_membership bibliophilly $id2

    csvfile=${TEMP_FILE}.1
    echo 'project_tag,document_base_dir,collection_tag' > $csvfile
    echo "bibliophilly,mscodex123,pennmss" >> $csvfile
    echo "bibliophilly,mscodex124,pennmss" >> $csvfile

    output=`op-proj bulk-rm $csvfile`

    status=$?
    if [ $status != 0 ]
    then
        echo "$output"
    fi
    assertEquals 0 $status
    assertNumberOfMatchingLines "$output" 'Removed document .*from project' 2
    assertNotMatch "$output" 'ERROR'
}

testBulkRmByDocumentIDWithErrors() {
    insert_document mscodex123 pennmss
    insert_document mscodex124 pennmss
    id1=`get_document_id mscodex123 pennmss`
    id2=`get_document_id mscodex124 pennmss`
    add_project_membership bibliophilly $id1
    add_project_membership bibliophilly $id2


    csvfile=${TEMP_FILE}.3
    echo 'project_tag,document_id' > $csvfile

    # 2 good lines
    echo "bibliophilly,${id1}" >> $csvfile
    echo "bibliophilly,${id2}" >> $csvfile

    # 3 ERROR lines
    # use non-existent id
    id3=$((id2 + 1)) # <= bad id
    echo "bibliophilly,${id3}" >> $csvfile
    # use non-existent project
    echo "FALSE_PROJECT,${id2}" >> $csvfile
    # try to remove document second time;
    # should have error 'Document not in project'
    echo "bibliophilly,${id2}" >> $csvfile

    output=`op-proj bulk-rm $csvfile`
    status=$?
    if [ $status != 0 ]
    then
        echo "$output"
    fi
    assertEquals 0 $status
    assertNumberOfMatchingLines "$output" 'Removed document .*from project' 2
    assertNumberOfMatchingLines "$output" 'Unknown document' 1
    assertNumberOfMatchingLines "$output" 'Unknown project' 1
    assertNumberOfMatchingLines "$output" 'Document not in project' 1
}

testBulkRmByDocumentBaseDirWithErrors() {
    insert_document mscodex123 pennmss
    insert_document mscodex124 pennmss
    id1=`get_document_id mscodex123 pennmss`
    id2=`get_document_id mscodex124 pennmss`
    add_project_membership bibliophilly $id1
    add_project_membership bibliophilly $id2

    csvfile=${TEMP_FILE}.1
    echo 'project_tag,document_base_dir,collection_tag' > $csvfile

    # Insert 2 good lines
    echo "bibliophilly,mscodex123,pennmss" >> $csvfile
    echo "bibliophilly,mscodex124,pennmss" >> $csvfile

    # ERROR lines
    # use non-existent base_dir
    echo "bibliophilly,mscodex125,pennmss" >> $csvfile
    # use non-existent project
    echo "FALSE_PROJECT,mscodex124,pennmss" >> $csvfile
    # try to remove document second time;
    # should have error 'Document not in project'
    echo "bibliophilly,mscodex124,pennmss" >> $csvfile

    output=`op-proj bulk-rm $csvfile`
    status=$?
    if [ $status != 0 ]
    then
        echo "$output"
    fi
    assertEquals 0 $status
    assertNumberOfMatchingLines "$output" 'Removed document .*from project' 2
    assertNumberOfMatchingLines "$output" 'Unknown document' 1
    assertNumberOfMatchingLines "$output" 'Unknown project' 1
    assertNumberOfMatchingLines "$output" 'Document not in project' 1
}

# Run shunit
. $shunit
