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
    test_no_extras   = os.path.join(settings.PROJECT_PATH, 'test/data/json/mscodex1223_no_extra.json')

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_init(self):
        self.assertIsInstance(FileList(TestFileList.test_file_list), FileList)

    def test_file_lists(self):
        lst = FileList(TestFileList.test_file_list)
        self.assertIsInstance(lst.files(FileList.DOCUMENT), list)
        self.assertIsInstance(lst.files(FileList.EXTRA), list)

    def test_no_extras_has_empty_list(self):
        lst = FileList(TestFileList.test_no_extras)
        self.assertIsInstance(lst.files(FileList.EXTRA), list)

    def test_document_count_not_zero(self):
        self.assertGreater(FileList(TestFileList.test_file_list).count(), 0)

    def test_extras_count_not_zero(self):
        self.assertGreater(FileList(TestFileList.test_file_list).count(FileList.EXTRA), 0)

    def test_extras_count_is_zero(self):
        self.assertEqual(FileList(TestFileList.test_no_extras).count(FileList.EXTRA), 0)

    def test_file_data_is_correct_type(self):
        self.assertIsInstance(FileList(TestFileList.test_file_list).files()[0], FileList.FileData)


if __name__ == '__main__':
    unittest.main()
