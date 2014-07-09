#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
from django.utils import unittest
from django.test import TestCase
from django.conf import settings

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))
from openn.openn_exception import OPennException
from openn.xml.openn_tei import OPennTEI

class TestOPennTEI(TestCase):


    test_partial_tei = os.path.join(os.path.dirname(__file__), 'data/xml/ms1223_PARTIAL_TEI.xml')

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_get_call_number(self):
        openn_tei = OPennTEI(TestOPennTEI.test_partial_tei)
        self.assertEqual('Ms. Codex 1223', openn_tei.call_number)

if __name__ == '__main__':
    unittest.main()
