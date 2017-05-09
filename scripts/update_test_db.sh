#!/usr/bin/env bash

# Not sure this should be a script. -- it should only be run on the development machine.


trap "cleanup; exit 1" 1 2 3 10 13 15
trap "cleanup; exit" 0

this_dir=$(cd `dirname $0`; pwd)
DB_NAME=openn
DB_USER=openn
DB_DUMP="${this_dir}/../openn-`date +%Y%m%d%H%M%S`.dmp"
cmd=`basename $0`
RESTORE_DB=

MANAGE_COMMAND="${this_dir}/../manage.py"

PATH="${this_dir}/../bin":$PATH

cleanup() {
  shopt -u nocasematch
  if [[ -f "$DB_DUMP" ]]; then
    if [[ "$RESTORE_DB" = "TRUE" ]]; then
      echo "[$cmd] Restoring original database from '$DB_DUMP'"
      mysql -u $DB_USER $DB_NAME < "$DB_DUMP"
    fi
    echo "[$cmd] Gzipping database dump file: $DB_DUMP"
    gzip "$DB_DUMP"
  fi
}

# On a development machine, to update the test.sql fixtures, do the following:

# dump the openn database to openn.dmp for safekeeping:
echo "[$cmd] Dumping database $DB_NAME to $DB_DUMP"
if ! mysqldump -u $DB_USER $DB_NAME > $DB_DUMP; then
  echo "[$cmd] Error dumping $DB_NAME to $DB_DUMP; exiting"
  exit 1
fi

echo "[$cmd] This will drop and recreate the database $DB_NAME. Proceed? [NO|yes]:"
read proceed
[[ $proceed ]] || proceed=NO
shopt -s nocasematch
if [[ "$proceed" =~ ^yes$ ]]; then
  echo "[$cmd] User entered $proceed; recreating database $DB_NAME"
else
  echo "[$cmd] Proceed is '$proceed'; exiting"
  exit 1
fi
shopt -u nocasematch

echo "[$cmd] Recreating database $DB_NAME"
echo "[$cmd] At the prompt enter root mysql user's password"
if ! mysql -u root -p < $this_dir/recreate_dev_db.sql; then
  echo "[$cmd] Error recreating database $DB_USER"
  exit 1
fi

RESTORE_DB=TRUE

#Load the test fixture into openn
test_fixture="$this_dir/../test/fixtures/test.sql"
echo "[$cmd] Loading test fixture: $test_fixture"
if ! mysql -u $DB_USER $DB_NAME < "$test_fixture"; then
  echo "[$cmd] Error loading test fixture: $test_fixture"
  exit 1
fi

# Run the migrations
echo "[$cmd] Migrating test database"
if ! "$MANAGE_COMMAND" migrate openn; then
  echo "[$cmd] Error migrating database"
  exit 1
fi

# update the repositories list
echo "[$cmd] Updating repos"
if ! op-repo update; then
  echo "[$cmd] Error updating repos"
  exit 1
fi

# update the curated collections list
echo "[$cmd] Updating curated collections"
if ! op-curt update; then
  echo "[$cmd] Error updating curated collections"
  exit 1
fi

# dump the updated data to the fixture SQL
echo "[$cmd] Dumping the database $DB_NAME to "
mysqldump -u $DB_USER $DB_NAME > "$test_fixture"

json_dump="$this_dir/../openn/fixtures/test.json"
echo "[$cmd] Dumping schema to JSON: $json_dump"
if ! "$MANAGE_COMMAND" dumpdata | $this_dir/fix_test_json.py > "$json_dump"; then
  echo "[$cmd] Error dumping schema to '$json_dump'"
  exit 1
fi

echo "[$cmd] Success; test database updated"

# # restore openn
# $ mysql -u openn openn < openn.dmp

# # clean up
# $ rm openn.dmp

### EXIT
# http://stackoverflow.com/questions/430078/shell-script-templates
cleanup
trap 0
exit 0
