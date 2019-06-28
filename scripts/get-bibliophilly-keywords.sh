#!/usr/bin/env bash

# Upate the bibliophilly-keywords repo or clone it if it doesn't exist.

cmd=`basename $0`

this_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
outdir="${1}"

[[ $outdir ]] || { echo "Please provide an OUTDIR argument"; exit 1; }

if [ -d "$outdir" ]; then
  echo "[$cmd] Updating keywords"
  cd "$outdir"
  git pull --progress
  if [[ $? -ne 0 ]]; then
    echo "WARNING: Unable to update get repo; using cached copy"
  fi
else
  echo "[$cmd] Retrieving keywords"
  bibliophilly_repo="https://github.com/leoba/bibliophilly-keywords.git"
  git clone --progress "${bibliophilly_repo}" "$outdir"
fi
