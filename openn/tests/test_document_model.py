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
from openn.models import *
from openn.repository.configs import Configs
from openn.tests.openn_test_case import OPennTestCase

class TestDocumentModel(OPennTestCase):
    configs = Configs(settings.REPOSITORIES)

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_init(self):
        self.assertIsInstance(Document(), Document)

    def test_is_live(self):
        ljs = self.configs.get_repository('ljs').repository()

        document = Document(repository = ljs, base_dir = 'ljs22')
        self.assertTrue(document.is_live())
