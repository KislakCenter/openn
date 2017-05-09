#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json

from django.utils import unittest
from django.test import TestCase
from django.conf import settings

from openn.prep.op_workbook import OPWorkbook
from openn.prep.validatable_sheet import ValidatableSheet
from openn.tests.openn_test_case import OPennTestCase

class TestValidatableSheet(OPennTestCase):
    this_dir                 = os.path.dirname(__file__)
    diaries_dir              = os.path.join(this_dir, 'data/diaries')
    sheets_dir               = os.path.join(this_dir, 'data/sheets')
    valid_workbook           = os.path.join(sheets_dir, 'valid_workbook.xlsx')
    valid_workbook_unicode   = os.path.join(sheets_dir, 'valid_with_unicode.xlsx')

    url1 = 'http://id.loc.gov/authorities/names/n50049445.html'
    url2 = 'http://id.loc.gov/authorities/subjects/sh99002320.html'
    url3 = 'http://id.loc.gov/authorities/subjects/sh85060757'
    url4 = 'http://id.loc.gov/authorities/subjects/sh2010118889'
    url5 = 'https://openpyxl.readthedocs.org/en/latest/api/openpyxl.worksheet.html?highlight=min_col#openpyxl.worksheet.worksheet.Worksheet.min_col'

    pacscl_diairies_json    = os.path.join(sheets_dir, 'pacscl_diaries.json')

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def get_config(self):
        return json.load(open(self.pacscl_diairies_json))

    def test_init(self):
        sheet = OPWorkbook(self.valid_workbook, self.get_config()).description
        self.assertIsInstance(sheet, ValidatableSheet)

    def test_is_valid_uri(self):
        for url in [ self.url1, self.url2, self.url3, self.url4, self.url5 ]:
            self.assertTrue(ValidatableSheet.is_valid_uri(url))

    def test_is_not_valid_uri(self):
        self.assertFalse(ValidatableSheet.is_valid_uri("car money"))

    def test_is_valid_year(self):
        for year in (2013, 013, 3000, -5000, 2):
            self.assertTrue(ValidatableSheet.is_valid_year(year), ("%d should be a valid year" % (year,)))

    def test_is_not_valid_year(self):
        for year in (2013.3, 'car', 3001, -5001):
            self.assertFalse(ValidatableSheet.is_valid_year(year), ("%s should not be a valid year" % (str(year),)))

    def test_is_valid_email(self):
        self.assertTrue(ValidatableSheet.is_valid_email('joe@example.com'))

    def test_is_valid_lang(self):
        for x in ('eng', 'eng ', ' eng ', 'en'):
            self.assertTrue(ValidatableSheet.is_valid_lang(x), ('%s should be a valid lang' % x))

    def test_is_not_valid_lang(self):
        for x in ('engx', 'x ', ' e ', 'enx'):
            self.assertFalse(ValidatableSheet.is_valid_lang(x), ('%s should not be a valid lang' % x))

    def test_is_valid_integer(self):
        for x in (1, 4, '4', ' 4 ', 300, '', '    ', None, 999999999999999):
            self.assertTrue(ValidatableSheet.is_valid_integer(x), ('%r should be a valid integer' % x))

    def test_is_not_valid_integer(self):
        for x in (1.1, 4.0, '4x', ' dog ', 'None'):
            self.assertFalse(ValidatableSheet.is_valid_integer(x), ('%r should not be a valid integer' % x))

    def test_handles_unicode(self):
        workbook = OPWorkbook(self.valid_workbook_unicode, self.get_config())

        workbook.validate_description()
        workbook.validate_pages()
