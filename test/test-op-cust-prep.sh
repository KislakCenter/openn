#!/usr/bin/env sh

THIS_DIR=`dirname $0`
source $THIS_DIR/shunit_helper

TEMPLATE_TEI=$TEST_DATA_DIR/xml/Archie_TEI.xml

# suite() {
#     suite_addTest testRun
# }

setUp() {
    # make sure the database is empty
    clear_tables
    update_output=`op-repo update`
    if [[ $? -ne 0 ]]
    then
        echo "$output"
    fi
}

tearDown() {
    mysqldump -u openn openn_test > junk.sql
    clear_tables
}

testRun() {
    output=`op-cust-prep private1-dirlesstei ArchimedesPalimpsest $TEMPLATE_TEI`

    status=$?
    if [ $status != 0 ]
    then
        echo "$output"
    fi
    assertEquals 0 $status
}

# Run shunit
. $shunit
