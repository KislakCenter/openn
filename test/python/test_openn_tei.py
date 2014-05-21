#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))
from openn.openn_exception import OPennException
from openn.xml.openn_tei import OPennTEI

class TestOPennTEI(unittest.TestCase):


    this_dir         = os.path.dirname(os.path.abspath(__file__))
    test_partial_tei = os.path.join(this_dir, '../data/xml/ms1223_PARTIAL_TEI.xml')

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_get_shelf_mark(self):
        openn_tei = OPennTEI(TestOPennTEI.test_partial_tei)
        self.assertEqual('Ms. Codex 1223', openn_tei.shelf_mark())

if __name__ == '__main__':
    unittest.main()
