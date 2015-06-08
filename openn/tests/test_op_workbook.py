#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json

from django.utils import unittest
from django.test import TestCase
from django.conf import settings
from django.core.exceptions import ValidationError

from openn.prep.op_workbook import OPWorkbook

class TestOPWorkbook(TestCase):
    this_dir                = os.path.dirname(__file__)
    diaries_dir             = os.path.join(this_dir, 'data/diaries')

    pacscl_diairies_json    = os.path.join(this_dir, '../prep/pacscl_diaries.json')
    helen_griffith          = os.path.join(diaries_dir, 'bryn_mawr/HelenGriffith_Diary.xlsx')

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def get_config(self):
        return json.load(open(self.pacscl_diairies_json))

    def test_init(self):
        sheet = OPWorkbook(self.helen_griffith, self.get_config())
        self.assertIsInstance(sheet,OPWorkbook)

    def test_validate_description(self):
        sheet = OPWorkbook(self.helen_griffith, self.get_config())
        sheet.validate_description()
        self.assertFalse(sheet.has_description_errors())

if __name__ == '__main__':
    unittest2.main()
