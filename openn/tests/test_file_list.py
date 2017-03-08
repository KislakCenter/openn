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
from openn.tests.openn_test_case import OPennTestCase

class TestFileList(OPennTestCase):


    file_list_path   = os.path.join(os.path.dirname(__file__), 'data/json/mscodex1223_file_list.json')
    no_extras_path   = os.path.join(os.path.dirname(__file__), 'data/json/mscodex1223_no_extra.json')

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_init(self):
        self.assertIsInstance(FileList(TestFileList.file_list_path), FileList)

    def file_list_paths(self):
        lst = FileList(TestFileList.file_list_path)
        self.assertIsInstance(lst.files(FileList.DOCUMENT), list)
        self.assertIsInstance(lst.files(FileList.EXTRA), list)

    def no_extras_path_has_empty_list(self):
        lst = FileList(TestFileList.no_extras_path)
        self.assertIsInstance(lst.files(FileList.EXTRA), list)

    def test_document_count_not_zero(self):
        self.assertGreater(FileList(TestFileList.file_list_path).count(), 0)

    def test_extras_count_not_zero(self):
        self.assertGreater(FileList(TestFileList.file_list_path).count(FileList.EXTRA), 0)

    def test_extras_count_is_zero(self):
        self.assertEqual(FileList(TestFileList.no_extras_path).count(FileList.EXTRA), 0)

    def test_file_data_is_correct_type(self):
        self.assertIsInstance(FileList(TestFileList.file_list_path).files()[0], FileList.FileData)

    def test_file_list_has_types(self):
        self.assertEqual(FileList(TestFileList.file_list_path).types, [ 'document', 'extra' ])

    def test_paths(self):
        fl = FileList(TestFileList.file_list_path)
        for file in fl.files():
            base, ext = os.path.splitext(file.filename)
            for dtype in [ 'master', 'web', 'thumb' ]:
                file.add_deriv("%s_%s%s" % (base, dtype, ext), dtype)
        self.assertIsInstance(fl.paths, list)
        # should be three paths for each doc file and 1 for each extra
        expected_count = fl.count('document') * 3 + fl.count('extra')
        self.assertEqual(len(fl.paths), expected_count)

if __name__ == '__main__':
    unittest.main()
