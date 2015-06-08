#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json
import re
import shutil
import sys
import glob

from django.utils import unittest
from django.test import TestCase
from django.conf import settings
from django.core.exceptions import ValidationError
from pprint import PrettyPrinter

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))
from openn.openn_exception import OPennException
from openn.prep.spreadsheet_prep import SpreadsheetPrep
from openn.prep.file_list import FileList
from openn.xml.openn_tei import OPennTEI
from openn.prep.prep_setup import PrepSetup
from openn.models import *

class TestSpreadsheetPrep(TestCase):

    this_dir                 = os.path.dirname(__file__)
    pacscl_diairies_config   = json.load(open(os.path.join(this_dir, '../prep/pacscl_diaries.json')))

    staging_dir              = os.path.join(os.path.dirname(__file__), 'staging')
    diaries_dir              = os.path.join(os.path.dirname(__file__), 'data/diaries')
    bryn_mawr_dir            = os.path.join(diaries_dir, 'bryn_mawr')
    haverford_dir            = os.path.join(diaries_dir, 'haverford')
    swarthmore_dir           = os.path.join(diaries_dir, 'swarthmore')

    haverfordcollege_975_dir = os.path.join(diaries_dir, 'haverford/JournalsAndDiaries_975')

    template_dir             = haverfordcollege_975_dir
    staged_source            = os.path.join(staging_dir, 'JournalsAndDiaries_975')
    haverford_coll           = 'haverford'
    pp                       = PrettyPrinter(indent=2)

    def setUp(self):
        if not os.path.exists(TestSpreadsheetPrep.staging_dir):
            os.mkdir(TestSpreadsheetPrep.staging_dir)

    def tearDown(self):
        if os.path.exists(TestSpreadsheetPrep.staging_dir):
            shutil.rmtree(TestSpreadsheetPrep.staging_dir)

    def touch(self, filename, times=None):
        with(open(filename,'a')):
            os.utime(filename, times)

    def assertHasFile(self,file_list, group, path):
        for info in file_list[group]:
            if info['filename'] == path:
                return True
        raise AssertionError("Expected file: '%s' in group: '%s'" % (path,group))

    def assertNotHasFile(self,file_list, group, path):
        for info in file_list[group]:
            if info['filename'] == path:
                raise AssertionError("Should not have file: '%s' in group: '%s'" % (path,group))

    def pprint(self,thing):
        TestSpreadsheetPrep.pp.pprint(thing)

    def stage_template(self):
        shutil.copytree(TestSpreadsheetPrep.template_dir, TestSpreadsheetPrep.staged_source)
        self.touch(os.path.join(TestSpreadsheetPrep.staged_source, 'somefile.tif'))

    def test_run(self):
        # setup
        self.stage_template()
        doc = PrepSetup().prep_document(TestSpreadsheetPrep.haverford_coll,
                                        'JournalsAndDiaries_975')
        prep = SpreadsheetPrep(TestSpreadsheetPrep.staged_source,
                               TestSpreadsheetPrep.haverford_coll,
                               doc,
                               self.pacscl_diairies_config)
        # run
        prep.prep_dir()

if __name__ == '__main__':
    unittest.main()
