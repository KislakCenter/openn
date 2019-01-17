# -*- coding: utf-8 -*-
import os
from glob import glob
import fnmatch
import re
import logging
import subprocess

from openn.openn_settings import OPennSettings
from openn.prep.status import Status
from openn.openn_exception import OPennException
from openn.xml.openn_tei import OPennTEI

"""Validate a directory based  on configuration.

Validation is a set of regular expression strings to compare to a
given directory. The script will walk the directory and test each file
and directory.


        {
            'valid_names': ['*.tif', 'bibid.txt'],
            'invalid_names': ['CaptureOne', 'Output', '*[()]*'],
            'required_names': ['*.tif', 'bibid.txt'],
        },


  - valid_names: list of valid file and directory glob patterns; if
    None or [], then no file names are permitted; globs are converted
    to regular expressions by fnmatch

  - invalid_names: list of invalid file and directory glob patterns;
    if None or [], then any file or directory name is permitted; globs
    are converted to regular expressions by fnmatch

  - required_names: list of glob patterns that must be present; if
    None or [], then no files are considered required; glob.glob()
    is used to find matching files

Note that `valid_names` and `invalid_names` complement each other and
may even be redundant. In the above example, a subdirectory named
'CaptureOne' would fail both the 'valid_names' and the 'invalid_names'
tests.  On the other hand, the 'invalid_names' pattern '*[()]*'
disallows any object names with parentheses and is needed to exclude a
file name like 'somefile(1).tif'.

"""
class PackageValidation(object):

    # These are globs for system files that should be regarded as
    # valid for purposes of the valid name check; they get added to the
    # `valid_names` glob list.
    SYSTEM_FILE_GLOBS = [ 'status.txt' ]

    def __init__(self, valid_names=[], invalid_names=[], required_names=[]):
        "Initialize this PackageValidation object"
        self._valid_name_res   = self.build_res(valid_names + self.SYSTEM_FILE_GLOBS)
        self._invalid_name_res = self.build_res(invalid_names)
        self._required_names   = required_names or []

    def build_res(self, globs):
        if not globs or len(globs) == 0:
            return []
        res = [ re.compile(fnmatch.translate(g)) for g in globs ]
        return res

    def validate(self, pkgdir):
        errors = []

        # don't validate if pkg is already being processed
        status_txt = os.path.join(pkgdir, 'status.txt')
        if os.path.exists(status_txt):
            return errors

        names = self.check_valid_names(pkgdir)
        if len(names) > 0:
            errors.append('VALID NAME CHECK: The following not found in valid name list: %s' % ('; '.join(names),))
        names = self.check_invalid_names(pkgdir)
        if len(names) > 0:
            errors.append('INVALID NAME CHECK: The following matched invalid name patterns: %s' % ('; '.join(names),))
        globs = self.check_required(pkgdir)
        if len(globs) > 0:
            errors.append('REQUIRED NAME CHECK: The following required file types not found: %s' % ('; '.join(globs),))
        return errors

    def check_required(self, pkgdir):
        errors  = []
        for g in self._required_names:
            path = os.path.join(pkgdir,g)
            if len(glob(path)) == 0:
                errors.append(g)
        return errors

    def check_invalid_names(self, pkgdir):
        errors = []
        for root, dirs, files in os.walk(pkgdir):
            for d in dirs:
                if self.is_in_list(d, self._invalid_name_res):
                    errors.append(d)
            for f in files:
                if self.is_in_list(f, self._invalid_name_res):
                    errors.append(f)
        return errors

    def check_valid_names(self, pkgdir):
        errors = []
        for root, dirs, files in os.walk(pkgdir):
            for d in dirs:
                if not self.is_in_list(d, self._valid_name_res):
                    errors.append(d)
            for f in files:
                if not self.is_in_list(f, self._valid_name_res):
                    errors.append(f)
        return errors

    def is_in_list(self, name, name_res):
        for name_re in name_res:
            if name_re.search(name):
                return True
        return False
