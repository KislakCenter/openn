#!/usr/bin/env bash

# Not sure this should be a script. -- it should only be run on the development machine.

trap "cleanup; exit 1" 1 2 3 10 13 15
trap "cleanup; exit" 0


cat <<EOF

# On a development machine, to update the test.sql fixtures with new
# collections. Do the following:

# dump the openn database to openn.dmp for safekeeping:
$ mysqldump -u openn openn > openn.dmp

# Load the test fixture into openn
$ mysql -u openn openn < test/fixtures/test.sql

# update the collection list
$ bin/op-coll update

# dump the updated data to the fixture SQL
$ mysqldump -u openn openn > test/fixtures/test.sql

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