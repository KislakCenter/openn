#!/usr/bin/env sh

THIS_DIR=`dirname $0`
source $THIS_DIR/shunit_helper

# suite() {
#     # suite_addTest testRun
# }

setUp() {
  # make sure the database is empty
  clear_tables
  mysql -u $OPENN_DB_USER --default-character-set=utf8 openn_test < $THIS_DIR/fixtures/test.sql
}

tearDown() {
  clear_tables
}

testList() {
  output=`op-repo list`
  status=$?
  if [ $status != 0 ]; then echo "$output"; fi
  assertEquals 0 $status
  assertMatch "$output" "pennmss"
}

testDetails() {
  output=`op-repo details pennmss`
  status=$?
  if [ $status != 0 ]; then echo "$output"; fi
  assertEquals 0 $status
  assertMatch "$output" "pennmss"
}

testUpdate() {
  output=`op-repo update`
  status=$?
  if [ $status != 0 ]; then echo "$output"; fi
  assertEquals 0 $status
  assertMatch "$output" "Repository already exists"
}

# Run shunit
. $shunit