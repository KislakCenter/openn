#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from django.utils import unittest
from django.test import TestCase
from django.conf import settings
from django.core.exceptions import ValidationError

from openn.prep.op_spreadsheet import OPSpreadsheet

class TestOpSpreadsheet(TestCase):
    this_dir                = os.path.dirname(__file__)
    diaries_dir             = os.path.join(this_dir, 'data/diaries')

    helen_griffith          = os.path.join(diaries_dir, 'bryn_mawr/HelenGriffith_Diary.xlsx')
    mary_ayer               = os.path.join(diaries_dir, 'bryn_mawr/MaryAyer_Diary.xlsx')
    mww_diary_vol10         = os.path.join(diaries_dir, 'bryn_mawr/MWW_Diary_Vol10.xlsx')
    mww_diary_vol11         = os.path.join(diaries_dir, 'bryn_mawr/MWW_Diary_Vol11.xlsx')
    mww_diary_vol12         = os.path.join(diaries_dir, 'bryn_mawr/MWW_Diary_Vol12.xlsx')
    mww_diary_vol9          = os.path.join(diaries_dir, 'bryn_mawr/MWW_Diary_Vol9.xlsx')
    pacscl_coates_sharpless = os.path.join(diaries_dir, 'haverford/Account of Coates, Shapless, etc/PACSCL metadata.xlsx')
    william_allinson_v1     = os.path.join(diaries_dir, 'haverford/Allinson, William/PACSCL metadata v1.xlsx')
    william_allinson_v2     = os.path.join(diaries_dir, 'haverford/Allinson, William/PACSCL metadata v2.xlsx')
    william_allinson_v3     = os.path.join(diaries_dir, 'haverford/Allinson, William/PACSCL metadata v3.xlsx')
    david_bacon             = os.path.join(diaries_dir, 'haverford/Bacon, David/PACSCL metadata.xlsx')
    joseph_sampson          = os.path.join(diaries_dir, 'haverford/Sansom, Joseph/PACSCL metadata.xlsx')
    swayne                  = os.path.join(diaries_dir, 'haverford/Swayne/PACSCL metadata.xlsx')
    xls_cooper              = os.path.join(diaries_dir, 'swarthmore/Cooper/PACSCL_Cooper.xls')
    xls_pierce              = os.path.join(diaries_dir, 'swarthmore/Pierce/PACSCL_Pierce.xls')
    xls_sharpless           = os.path.join(diaries_dir, 'swarthmore/Sharpless/PACSCL_Sharpless.xls')

    config_json             = os.path.join(diaries_dir, 'config.json')
    url1 = 'http://id.loc.gov/authorities/names/n50049445.html'
    url2 = 'http://id.loc.gov/authorities/subjects/sh99002320.html'
    url3 = 'http://id.loc.gov/authorities/subjects/sh85060757'
    url4 = 'http://id.loc.gov/authorities/subjects/sh2010118889'
    url5 = 'https://openpyxl.readthedocs.org/en/latest/api/openpyxl.worksheet.html?highlight=min_col#openpyxl.worksheet.worksheet.Worksheet.min_col'

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def get_config(self):
        return settings.SPREADSHEET_FIELDS

    def test_init(self):
        sheet = OPSpreadsheet(self.helen_griffith, self.get_config())
        self.assertIsInstance(sheet,OPSpreadsheet)

    def test_validate_description(self):
        sheet = OPSpreadsheet(self.helen_griffith, self.get_config())
        sheet.validate_description()
        # print sheet.validation_errors
        self.assertFalse(sheet.has_description_errors())

    def test_is_valid_uri(self):
        for url in [ self.url1, self.url2, self.url3, self.url4, self.url5 ]:
            self.assertTrue(OPSpreadsheet.is_valid_uri(url))

    def test_is_not_valid_uri(self):
        self.assertFalse(OPSpreadsheet.is_valid_uri("car money"))

    def test_is_valid_year(self):
        for year in (2013, 013, 3000, -5000, 2):
            self.assertTrue(OPSpreadsheet.is_valid_year(year), ("%d should be a valid year" % (year,)))

    def test_is_not_valid_year(self):
        for year in (2013.3, 'car', 3001, -5001):
            self.assertFalse(OPSpreadsheet.is_valid_year(year), ("%s should not be a valid year" % (str(year),)))

    def test_is_valid_email(self):
        self.assertTrue(OPSpreadsheet.is_valid_email('joe@example.com'))

    def test_is_valid_lang(self):
        for x in ('eng', 'eng ', ' eng ', 'en'):
            self.assertTrue(OPSpreadsheet.is_valid_lang(x), ('%s should be a valid lang' % x))

    def test_is_not_valid_lang(self):
        for x in ('engx', 'x ', ' e ', 'enx'):
            self.assertFalse(OPSpreadsheet.is_valid_lang(x), ('%s should not be a valid lang' % x))


if __name__ == '__main__':
    unittest2.main()
