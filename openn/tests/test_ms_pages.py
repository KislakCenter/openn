#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
from django.utils import unittest
from django.test import TestCase
from django.conf import settings

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))
from openn.openn_exception import OPennException
from openn.prep.ms_pages import MSPages
from openn.models import *

class TestMSPages(TestCase):


    def setUp(self):
        pass

    def tearDown(self):
        pass

    @property
    def document(self):
        if getattr(self,'doc', None) is None:
            self.doc = Document(call_number = 'MS Codex 123',
                    collection = 'medren',
                    title = 'Title of the Ms.',
                    base_dir = 'mscodex123')
            self.doc.full_clean()
            self.doc.save()
        return self.doc

    def test_init(self):
        self.assertIsInstance(MSPages(), MSPages)

    def test_browse_page(self):
        pages = MSPages()
        self.assertIsInstance(pages.browse_page(self.document.id), unicode)

if __name__ == '__main__':
    unittest.main()
