OPenn development setup
=======================

## Steps

- Get code
- Add env vars

Add file `$HOME/.opennrc`:

```bash
export OPENN_DB_NAME=openn
export OPENN_DB_USER=openn
export OPENN_DB_PASSWORD=FILLIN
export OPENN_DB_HOST=localhost
export OPENN_PACKAGE_DIR=$HOME/tmp/openn/packages
export OPENN_STAGING_DIR=$HOME/tmp/openn/staging
export OPENN_ARCHIVE_DIR=$HOME/tmp/openn/archive
```

- Setup environment
- Create database
- Load database
- Configure environment -- run `sh config.sh`

    * Requirements: exiftool, mysql, python2.6, virtualenv
