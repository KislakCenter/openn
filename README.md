OPenn scripts
=============

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
