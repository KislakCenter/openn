#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))
from openn.openn_exception import OPennException
from openn.prep.file_list import FileList

class TestFileList(unittest.TestCase):


    this_dir         = os.path.dirname(os.path.abspath(__file__))
    test_file_list   = os.path.join(this_dir, '../data/json/mscodex1223_file_list.json')

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_init(self):
        self.assertTrue(isinstance(FileList(TestFileList.test_file_list),FileList))

if __name__ == '__main__':
    unittest.main()
