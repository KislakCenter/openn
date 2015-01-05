#!/usr/bin/env sh

################################################################################
#
# Name:         test_allTests.sh
#
# Description:  Run all tests in containing folder matching test_*.sh, except
#               for self.
#
################################################################################

this_file=`basename $0`

for test in `dirname $0`/test*.sh
do
    [[ `basename $test` != $this_file ]] && echo "=== Running $test ===" && $test
done
