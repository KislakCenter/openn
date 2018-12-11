#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json
import pprint

from django.utils import unittest
from django.test import TestCase
from django.conf import settings
from django.core.exceptions import ValidationError

from openn.prep.op_workbook import OPWorkbook
from openn.tests.helpers import *
from openn.tests.openn_test_case import OPennTestCase

class TestOPWorkbook(OPennTestCase):
    this_dir                = os.path.dirname(__file__)
    sheets_dir              = os.path.join(this_dir, 'data/sheets')
    diaries_dir             = os.path.join(this_dir, 'data/diaries')

    pacscl_diairies_json    = os.path.join(sheets_dir, 'pacscl_diaries.json')
    bibliophilly_json       = os.path.join(sheets_dir, 'bibliophilly.json')
    muslim_world_json       = os.path.join(this_dir, 'data/muslim_world/muslimworld.json')

    valid_workbook          = os.path.join(sheets_dir, 'valid_workbook.xlsx')
    untrimmed_workbook      = os.path.join(this_dir, 'data/bibliophilly/FLPLewisE018/openn_metadata.xlsx')
    muslim_world_workbook   = os.path.join(this_dir, 'data/muslim_world/ms_or_24.xlsx')


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

    def test_muslimworld(self):
        config_dict = json.load(open(self.muslim_world_json))
        wkbk = OPWorkbook(self.muslim_world_workbook, config_dict)
        attrs = [key for key in config_dict['sheet_config']['pages']['fields']]
        wkbk.validate()
        self.assertFalse(wkbk.has_metadata_errors())

if __name__ == '__main__':
    unittest2.main()
