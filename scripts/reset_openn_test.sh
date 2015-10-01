#!/usr/bin/env bash

clear_tables() {
    tables="openn_derivative
        openn_image
        openn_version
        openn_prepstatus
        openn_document"

    for table in $tables
    do
        mysql -u openn openn_test -e "delete from $table"
    done
}

this_dir=`dirname $0`

mysql -u root -p -e "DROP DATABASE IF EXISTS openn_test;
CREATE DATABASE openn_test CHARACTER SET utf8 COLLATE utf8_unicode_ci;
GRANT ALL PRIVILEGES ON *.* TO 'openn'@'localhost' IDENTIFIED BY 'openn';
FLUSH PRIVILEGES;"

mysqldump -u openn openn > junk.sql

mysql -u openn openn_test < junk.sql

clear_tables

rm junk.sql
