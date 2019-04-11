#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from openn.tests.openn_test_case import OPennTestCase
from openn.version import Version

class TestVersion(OPennTestCase):
    def test_version(self):
        self.assertIsNotNone(Version.version())