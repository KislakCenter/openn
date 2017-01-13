#!/usr/bin/env bash

# Not sure this should be a script. -- it should only be run on the development machine.

trap "cleanup; exit 1" 1 2 3 10 13 15
trap "cleanup; exit" 0


cat <<EOF

# On a development machine, to update the test.sql fixtures, do the following:

# dump the openn database to openn.dmp for safekeeping:
$ mysqldump -u openn openn > openn.dmp

# Load the test fixture into openn
$ mysql -u openn openn < test/fixtures/test.sql

# Run the migrations
$ ./manage.py migrate openn

# update the repositories list
$ bin/op-repo update

# update the curated collections list
$ bin/op-curt update

# dump the updated data to the fixture SQL
$ mysqldump -u openn openn > test/fixtures/test.sql

# dump the data to JSON
$ ./manage.py dumpdata > openn/fixtures/test.json

# restore openn
$ mysql -u openn openn < openn.dmp

# clean up
$ rm openn.dmp


EOF

### EXIT
# http://stackoverflow.com/questions/430078/shell-script-templates
cleanup
trap 0
exit 0
