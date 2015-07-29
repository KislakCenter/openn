#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json

from django.utils import unittest
from django.test import TestCase
from django.conf import settings
from django.core.exceptions import ValidationError

from openn.prep.op_workbook import OPWorkbook
from openn.prep.pages_sheet import PagesSheet
from openn.prep.validatable_sheet import ValidatableSheet
from openn.tests.helpers import *

class TestPagesSheet(TestCase):
    this_dir                 = os.path.dirname(__file__)
    diaries_dir              = os.path.join(this_dir, 'data/diaries')
    sheets_dir               = os.path.join(this_dir, 'data/sheets')

    pages_workbook           = os.path.join(sheets_dir, 'pages.xlsx')
    pages_invalid_workbook   = os.path.join(sheets_dir, 'pages_invalid.xlsx')

    dummy_files = ( 'HelenGriffith_BMC_fc.tif',
                    'HelenGriffith_BMC_fpd.tif',
                    'HelenGriffith_BMC_0001.tif',
                    'HelenGriffith_BMC_0002.tif',
                    'HelenGriffith_BMC_0003.tif',
                    'HelenGriffith_BMC_0004.tif',
                    'HelenGriffith_BMC_0005.tif',
                    'HelenGriffith_BMC_0006.tif',
                    'HelenGriffith_BMC_0007.tif',
                    'HelenGriffith_BMC_0008.tif',
                    'HelenGriffith_BMC_0009.tif',
                    'HelenGriffith_BMC_0010.tif',
                    'HelenGriffith_BMC_0011.tif',
                    'HelenGriffith_BMC_0012.tif',
                    'HelenGriffith_BMC_0013.tif',
                    'HelenGriffith_BMC_0014.tif',
                    'HelenGriffith_BMC_0015.tif',
                    'HelenGriffith_BMC_0016.tif',
                    'HelenGriffith_BMC_0017.tif',
                    'HelenGriffith_BMC_0018.tif' )

    dummy_paths = [ os.path.join(sheets_dir, x) for x in dummy_files ]

    pages_config = json.load(open(os.path.join(sheets_dir, 'pages_config.json')))

    def setUp(self):
        pass

    def tearDown(self):
        for path in self.dummy_paths:
            if os.path.exists(path):
                os.remove(path)

    def test_init(self):
        sheet = OPWorkbook(self.pages_workbook, self.pages_config).pages
        self.assertIsInstance(sheet, ValidatableSheet)

    def test_validate(self):
        for path in self.dummy_paths: touch(path)
        sheet = OPWorkbook(self.pages_workbook, self.pages_config).pages
        sheet.validate()
        if len(sheet.errors) > 0: pp(sheet.errors)
        self.assertEqual(len(sheet.errors), 0)

    def test_required_if_other_nonempty(self):
        sheet = OPWorkbook(self.pages_invalid_workbook, self.pages_config).pages
        sheet.validate_requirement('serial_num')
        self.assertEqual(len(sheet.errors), 1)
        self.assertRegexpMatches(sheet.errors[0], r"'SERIAL_NUM' cannot be empty.* 'FILE_NAME'")

    def test_empty_if_other_nonempty(self):
        sheet = OPWorkbook(self.pages_invalid_workbook, self.pages_config).pages
        sheet.validate_blank('serial_num')
        self.assertEqual(len(sheet.errors), 1)
        self.assertRegexpMatches(sheet.errors[0], r"'SERIAL_NUM' must be empty.* 'FILE_NAME'")

    def test_value1_blank_if_toc1_empty(self):
        sheet = OPWorkbook(self.pages_invalid_workbook, self.pages_config).pages
        sheet.validate_blank('value1')
        self.assertEqual(len(sheet.errors), 1)
        self.assertRegexpMatches(sheet.errors[0], r"'VALUE1' must be empty.* 'TAG1'.*'September 24'")

    def test_value2_blank_if_toc2_empty(self):
        sheet = OPWorkbook(self.pages_invalid_workbook, self.pages_config).pages
        sheet.validate_blank('value2')
        self.assertEqual(len(sheet.errors), 1)
        self.assertRegexpMatches(sheet.errors[0], r"'VALUE2' must be empty.* 'TAG2'.*'September 27'")

    def test_value3_blank_if_toc3_empty(self):
        sheet = OPWorkbook(self.pages_invalid_workbook, self.pages_config).pages
        sheet.validate_blank('value3')
        self.assertEqual(len(sheet.errors), 1)
        self.assertRegexpMatches(sheet.errors[0], r"'VALUE3' must be empty.* 'TAG3'.*'March 15'")

    def test_value4_blank_if_toc4_empty(self):
        sheet = OPWorkbook(self.pages_invalid_workbook, self.pages_config).pages
        sheet.validate_blank('value4')
        self.assertEqual(len(sheet.errors), 1)
        self.assertRegexpMatches(sheet.errors[0], r"'VALUE4' must be empty.* 'TAG4'.*'Car'")

    def test_required_based_on_value_list_tag1_value1(self):
        sheet = OPWorkbook(self.pages_invalid_workbook, self.pages_config).pages
        sheet.validate_requirement('value1')
        self.assertEqual(len(sheet.errors), 1)
        self.assertRegexpMatches(sheet.errors[0], r"'VALUE1' cannot be empty.* 'TAG1'.*'TOC1'")

    def test_required_based_on_value_list_tag2_value2(self):
        sheet = OPWorkbook(self.pages_invalid_workbook, self.pages_config).pages
        sheet.validate_requirement('value2')
        self.assertEqual(len(sheet.errors), 1)
        self.assertRegexpMatches(sheet.errors[0], r"'VALUE2' cannot be empty.* 'TAG2'.*'ILL'")

    def test_notrequired_based_on_value_list_tag4_value4(self):
        sheet = OPWorkbook(self.pages_invalid_workbook, self.pages_config).pages
        sheet.validate_requirement('value4')
        self.assertEqual(len(sheet.errors), 0)

    def test_required_based_on_value_list_tag3_value3(self):
        sheet = OPWorkbook(self.pages_invalid_workbook, self.pages_config).pages
        sheet.validate_requirement('value3')
        self.assertEqual(len(sheet.errors), 1)
        self.assertRegexpMatches(sheet.errors[0], r"'VALUE3' cannot be empty.* 'TAG3'.*'TOC3'")

    def test_validate_uniqueness(self):
        sheet = OPWorkbook(self.pages_invalid_workbook, self.pages_config).pages
        sheet.validate_uniqueness('file_name')
        self.assertEqual(len(sheet.errors), 1)
        self.assertRegexpMatches(sheet.errors[0], r"'FILE_NAME' cannot have duplicate values; found:.*(2x)")
