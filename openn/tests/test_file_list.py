#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
from django.utils import unittest
from django.test import TestCase
from django.conf import settings

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))
from openn.openn_exception import OPennException
from openn.prep.file_list import FileList

class TestFileList(TestCase):


    test_file_list   = os.path.join(settings.PROJECT_PATH, 'test/data/json/mscodex1223_file_list.json')

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_init(self):
        self.assertIsInstance(FileList(TestFileList.test_file_list), FileList)

if __name__ == '__main__':
    unittest.main()
