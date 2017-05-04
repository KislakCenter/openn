#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json

from django.utils import unittest
from django.test import TestCase
from django.conf import settings
from django.core.exceptions import ValidationError

from openn.prep.op_workbook import OPWorkbook
from openn.tests.helpers import *

class TestOPWorkbook(TestCase):
    this_dir                = os.path.dirname(__file__)
    sheets_dir              = os.path.join(this_dir, 'data/sheets')
    diaries_dir             = os.path.join(this_dir, 'data/diaries')

    pacscl_diairies_json    = os.path.join(sheets_dir, 'pacscl_diaries.json')
    bibliophilly_json       = os.path.join(sheets_dir, 'bibliophilly.json')

    valid_workbook          = os.path.join(sheets_dir, 'valid_workbook.xlsx')
    untrimmed_workbook      = os.path.join(this_dir, 'data/bibliophilly/FLPLewisE018/openn_metadata.xlsx')


    def setUp(self):
        pass

    def tearDown(self):
        pass

    def get_config(self):
        return json.load(open(self.pacscl_diairies_json))

    def test_init(self):
        sheet = OPWorkbook(self.valid_workbook, self.get_config())
        self.assertIsInstance(sheet,OPWorkbook)

    def test_validate_description(self):
        sheet = OPWorkbook(self.valid_workbook, self.get_config())
        sheet.validate_description()
        self.assertFalse(sheet.has_description_errors())

    def test_validate_pages(self):
        sheet = OPWorkbook(self.valid_workbook, self.get_config())
        sheet.validate_pages()
        self.assertFalse(sheet.has_page_errors())

    def test_has_metadata_errors(self):
        sheet = OPWorkbook(self.valid_workbook, self.get_config())
        sheet.validate()
        self.assertFalse(sheet.has_metadata_errors())

    def test_untrimmed_workbook(self):
        wkbk = OPWorkbook(self.untrimmed_workbook, json.load(open(self.bibliophilly_json)))
        wkbk.validate()
        self.assertFalse(wkbk.has_metadata_errors())

if __name__ == '__main__':
    unittest2.main()
