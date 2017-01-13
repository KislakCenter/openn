# -*- coding: utf-8 -*-

import os
import sys
from django.utils import unittest
from django.test import TestCase
from django.conf import settings

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))
from openn.models import *
from openn.pages.document_data import DocumentData
from openn.repository.configs import Configs

class TestDocumentData(TestCase):
    fixtures = [ 'test.json' ]
    configs = Configs(settings.REPOSITORIES)
    pennmss_wrapper = configs.get_repository('pennmss')

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_pages(self):
        document = Document.objects.get(base_dir='mscodex1589')
        doc_data = DocumentData(document, self.pennmss_wrapper, 'html')
        self.assertTrue(len(doc_data.pages) > 0)

    def test_ms_item_pages(self):
        document = Document.objects.get(base_dir='mscodex1589')
        doc_data = DocumentData(document, self.pennmss_wrapper, 'html')
        # print "doc_data.ms_item_pages: %d" % len(doc_data.ms_item_pages)
        self.assertTrue(len(doc_data.ms_item_pages) > 0)

    def test_deco_note_pages(self):
        document = Document.objects.get(base_dir='mscodex1589')
        doc_data = DocumentData(document, self.pennmss_wrapper, 'html')
        # print "doc_data.deco_note_pages: %d" % len(doc_data.deco_note_pages)
        self.assertTrue(len(doc_data.deco_note_pages) > 0)
