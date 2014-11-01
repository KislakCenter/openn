#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import shutil
import sys
from django.utils import unittest
from django.test import TestCase
from django.conf import settings

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))
from openn.openn_exception import OPennException
from openn.md.dublin_core import DublinCore
from openn.models import *

class DCTest(DublinCore):
    def dc_identifier(self):
        return 'abc123'

    def dc_creator(self):
        return [ 'Smith, Joan', 'Brown, Charles' ]


class TestDublinCore(TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_init(self):
        self.assertIsInstance(DCTest(), DublinCore)

    def test_to_dict(self):
        dc = DCTest()
        self.assertEqual(len(dc.to_dict()), 2)

    def test_dc_creator(self):
        self.assertIn('Smith, Joan', DCTest().dc_creator())

    def test_dc_identifier(self):
        self.assertEqual('abc123', DCTest().dc_identifier())
