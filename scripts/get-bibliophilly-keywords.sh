#!/usr/bin/env bash

# Upate the bibliophilly-keywords repo or clone it if it doesn't exist.

cmd=`basename $0`

this_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
outdir="${this_dir}/../vendor/bibliophilly-keywords"

if [ -d "$outdir" ]; then
  echo "[$cmd] Updating keywords"
  cd "$outdir"
  git pull --progress
else
  echo "[$cmd] Retrieving keywords"
  bibliophilly_repo="https://github.com/leoba/bibliophilly-keywords.git"
  git clone --progress "${bibliophilly_repo}" "$outdir"
fi
