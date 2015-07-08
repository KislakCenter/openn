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
from openn.tests.helpers import *

class TestSpreadsheetPrep(TestCase):

    this_dir               = os.path.dirname(__file__)
    data_dir               = os.path.join(this_dir, 'data')
    sheets_dir             = os.path.join(data_dir, 'sheets')
    staging_dir            = os.path.join(os.path.dirname(__file__), 'staging')

    pacscl_diairies_json   = os.path.join(sheets_dir, 'pacscl_diaries.json')
    pacscl_diairies_config = json.load(open(os.path.join(sheets_dir, 'pacscl_diaries.json')))
    valid_workbook         = os.path.join(sheets_dir, 'valid_workbook.xlsx')

    template_image_names   = """HelenGriffith_BMC_fc.tif
                                 HelenGriffith_BMC_fpd.tif
                                 HelenGriffith_BMC_0001.tif
                                 HelenGriffith_BMC_0002.tif
                                 HelenGriffith_BMC_0003.tif
                                 HelenGriffith_BMC_0004.tif
                                 HelenGriffith_BMC_0005.tif
                                 HelenGriffith_BMC_0006.tif
                                 HelenGriffith_BMC_0007.tif
                                 HelenGriffith_BMC_0008.tif
                                 HelenGriffith_BMC_0009.tif
                                 HelenGriffith_BMC_0010.tif
                                """
    bad_description        = os.path.join(sheets_dir, 'template_bad_description')
    bad_pages              = os.path.join(sheets_dir, 'template_bad_pages')
    template_tiff          = os.path.join(data_dir, 'images/template_image.tif')
    template_dir           = os.path.join(sheets_dir, 'valid_template')
    staged_source          = os.path.join(staging_dir, 'XYZ_ABC_1')
    haverford_coll         = 'haverford'

    def setUp(self):
        if not os.path.exists(self.staging_dir):
            os.mkdir(self.staging_dir)

    def tearDown(self):
        if os.path.exists(self.staging_dir):
            shutil.rmtree(self.staging_dir)

    def assertHasFile(self,file_list, group, path):
        for info in file_list[group]:
            if info['filename'] == path:
                return True
        raise AssertionError("Expected file: '%s' in group: '%s'" % (path,group))

    def assertNotHasFile(self,file_list, group, path):
        for info in file_list[group]:
            if info['filename'] == path:
                raise AssertionError("Should not have file: '%s' in group: '%s'" % (path,group))

    def stage_template(self, template=None):
        if template is None: template = self.template_dir
        shutil.copytree(template, self.staged_source)
        for fname in self.template_image_names.split():
            destfile = os.path.join(self.staged_source, fname)
            shutil.copyfile(self.template_tiff, destfile)

    def test_run(self):
        # setup
        self.stage_template()
        doc = PrepSetup().prep_document(self.haverford_coll, 'XYZ_ABC_1')
        prep = SpreadsheetPrep(self.staged_source, self.haverford_coll, doc, self.pacscl_diairies_json)

        # run
        try:
            prep.prep_dir()
        except OPennException as oe:
            self.fail("Prep should raise no exception; got: %s" % (oe,))

        file_path = os.path.join(self.staged_source,'data', self.template_image_names.split()[0])
        self.assertTrue(os.path.exists(file_path), "File should exist: %s" % (file_path, ))

        file_path = os.path.join(self.staged_source, 'openn_metadata.xml')
        self.assertFalse(os.path.exists(file_path), "File should should have been removed: %s" % (file_path, ))

        file_path = os.path.join(self.staged_source, 'openn_metadata.xlsx')
        self.assertFalse(os.path.exists(file_path), "File should should have been removed: %s" % (file_path, ))

        file_path = os.path.join(self.staged_source, 'file_list.json')
        self.assertTrue(os.path.exists(file_path), "File should exist: %s" % (file_path, ))

        file_path = os.path.join(self.staged_source, 'PARTIAL_TEI.xml')
        self.assertTrue(os.path.exists(file_path), "File should exist: %s" % (file_path, ))

    def test_prep_dir_bad_description(self):
        self.stage_template(template=self.bad_description)
        doc = PrepSetup().prep_document(self.haverford_coll, 'XYZ_ABC_1')
        prep = SpreadsheetPrep(self.staged_source, self.haverford_coll, doc, self.pacscl_diairies_json)

        with self.assertRaises(OPennException) as oe:
            prep.prep_dir()

        self.assertIn('Language', str(oe.exception))

    def test_prep_dir_bad_pages(self):
        self.stage_template(template=self.bad_pages)
        doc = PrepSetup().prep_document(self.haverford_coll, 'XYZ_ABC_1')
        prep = SpreadsheetPrep(self.staged_source, self.haverford_coll, doc, self.pacscl_diairies_json)

        with self.assertRaises(OPennException) as oe:
            prep.prep_dir()

        self.assertIn('FILE_NAME', str(oe.exception))

    def test_prep_dir_missing_file(self):
        self.stage_template()
        doc = PrepSetup().prep_document(self.haverford_coll, 'XYZ_ABC_1')
        prep = SpreadsheetPrep(self.staged_source, self.haverford_coll, doc, self.pacscl_diairies_json)
        tiffs = glob.glob(os.path.join(self.staged_source, '*.tif'))
        os.remove(tiffs[0])
        with self.assertRaises(OPennException) as oe:
            prep.prep_dir()

        self.assertIn('FILE_NAME', str(oe.exception))

if __name__ == '__main__':
    unittest.main()
