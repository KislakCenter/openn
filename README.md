OPenn scripts
=============

## Configuration notes

Spreadsheets are configured via JSON files. This configuration is documented
in ValidatableSheet, the core spreadsheet class. These notes document a number
of optimizations to handle quirks some spreadsheets. Under certain
circumstances an Excel spreadsheet will use all columns or rows. So, for
example, for a book of 300 pages, the PyXL function `last_row` used by
ValidatableSheet to find the last row in a spreadsheet, will not return the
index of the last utilized row, but the last row of the spreadsheet, which for
XLSX files is 1,048,576. This creates all kinds of problems, not least of
which is that scripts never finish running. Also, some spreadsheets will have
cells that appear blank, but are not. These non-blank blank fields create
problems for validation under certain circumtances.

The following configurations are intended to prevent incorrect field
validation and to optimize field extraction.

#### Repeat limit

The sheet-level `repeat_limit` configuration value sets a repeating field
limit. This limit can be either a numerical value or based on a list of
fields.

For example,

        {
            "sheet_config": {
                "description": {
                    "sheet_name": "Description",
                    "data_offset": 2,
                    "heading_type": "row",
                    "repeat_limit": {
                        "fixed": 50
                    },
                    "max_column": 200,
                    "max_row": 500,
                    ...

Here the `repeat_limit` is `fixed` at 50 columns (columns because the sheet
has row headers at the left of the sheet, rather than column headers). The
search script that searches for repeating fields values won't look beyond 50
columns or the `max_colum` returned by PyXL, whichever number is smaller.

This is an example of dynamic repeat limit:


                ...
                "pages": {
                    "sheet_name": "Pages",
                    "data_offset": 1,
                    "heading_type": "column",
                    "repeat_limit": {
                        "fields": [ "file_name", "display_page" ]
                    },
                    "max_column": 200,
                    "max_row": 10000,
                    ...

Here the `repeat_limit` is determined based on the presence of repeating
values in the `file_name` and `display_page` columns. The last row of the
sheet serached for values will be the last row containing a `file_name` or
`display_page`, whichever is higher. These two fields are chosen because  the
pages sheet must have exactly the same number of values for both fields.

#### Max column and row values

These two configuration fields `max_column` and `max_row` set a sanity limit
on how far the application will search for field values. In the event that the
PyXL `max_column` or `max_row` is mistakenly some ridiculously high value, the
system will cap searching at these configured values. Both `max_column` and
`max_row` should be set to numbers that are well beyond any reasonable
location for valid spreadsheet data, but considerably lower than the allowable
spreadsheet maximums. In the "pages" example above, the `max_row` number is
10,000 which should be well more than any book's page numbers. If the number
is too low, though, it can can be changed via the configuration.

#### Hard coded configuration

The spreadsheet preparation class does not handle spreadsheets with headings
that extend beyond 300 rows or columns.  Should a spreadsheet used for  OPenn
have headings that go beyond 300 rows or columns, this code will need to be
changed.

## Install

Clone repo.

```bash
cd ~/scripts
git clone git@github.com:demery/openn.git
```

Install MySQL, python26-mysqldb, virtualenv using yum.

Create the virutalenv and install python libraries.

```bash
cd ~/scripts/openn
virtualenv-2.6 --prompt="(openn)" venv

# IMPORTANT! source the virtualenv
source venv/bin/activate

# install this fork of pyexiftool first (not available through pip
git clone git@github.com:demery/pyexiftool.git
cd pyexiftool
python setup.py install
cd ../
rm -rf pyexiftool

# install the remaining packages
pip install -r requirements.txt
```

Make sure the following env variables are set.

```bash
export OPENN_DB_NAME=openn
export OPENN_DB_USER=openn
export OPENN_DB_PASSWORD=<OPENN_DB_PASS>
export OPENN_DB_HOST=localhost
# OPENN_PACKAGE_DIR: where packages are staged for pushing to openn
export OPENN_PACKAGE_DIR=/path/to/openn/packages
# OPENN_STAGING_DIR: where html files are staged for pushing to openn
export OPENN_STAGING_DIR=$HOME/openn/site
export OPENN_SAXON_JAR=$HOME/path/to/saxon9he.jar
```

Create the directories if they don't exist.

```bash
mkdir -p /path/to/openn/packages
mkdir -p /path/to/openn/site
```

Create some database. (Instructions swiped from codeforkjeff.)

```sql
mysql -u root
CREATE DATABASE openn CHARACTER SET utf8 COLLATE utf8_unicode_ci;
CREATE USER 'openn'@'localhost' IDENTIFIED BY 'xxx';
GRANT ALL PRIVILEGES ON *.* TO 'openn'@'localhost';
FLUSH PRIVILEGES;
```

Run syncdb and migrate the database.

```bash
cd /path/to/openn
source venv/bin/activate
./manage.py syncdb
./manage.py migrate
```

Finally, add OPenn to your path.

```bash
PATH=$HOME/scripts/openn/bin:$PATH

export PATH
```

## Site structure

    0_ReadMe.html
    1_TechnicalReadMe.html
    3_Collections.html
    TOC_LJSchoenberg.html
    TOC_PennManuscripts.html
    TOC_PACSL_Diaries.html
    Data/
        LJSchoenbergManusripts/
            html
                ljs123.html
                ljs134.html
                ...
            ljs123/
            ljs134/
            ...
        PennManuscripts/
            ...
        PACSCL_Diaries/
            ...


## Backing up

`mysqldump -u DB_USER DB_NAME > /mnt/scratch01/openn/db_backups/openn_`date +%Y%m%dT%H%M%S%z`.dmp`

test
