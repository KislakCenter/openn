#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import shutil
from django.utils import unittest
from django.test import TestCase
from django.conf import settings

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))
from openn.openn_exception import OPennException
from openn.pages.browse import Browse
from openn.models import *

class TestBrowsePage(TestCase):
    fixtures = [ 'test.json' ]

    staging_dir      = os.path.join(os.path.dirname(__file__), 'staging')
    ljs270_tei       = os.path.join(os.path.dirname(__file__), 'data/xml/ljs270_TEI.xml')
    ljs454_tei       = os.path.join(os.path.dirname(__file__), 'data/xml/ljs454_TEI.xml')
    ljs471_tei       = os.path.join(os.path.dirname(__file__), 'data/xml/ljs471_TEI.xml')
    ljs498_tei       = os.path.join(os.path.dirname(__file__), 'data/xml/ljs498_TEI.xml')
    mscodex1589_tei  = os.path.join(os.path.dirname(__file__), 'data/xml/mscodex1589_TEI.xml')
    mscodex218_tei   = os.path.join(os.path.dirname(__file__), 'data/xml/mscodex218_TEI.xml')
    mscodex52_tei    = os.path.join(os.path.dirname(__file__), 'data/xml/mscodex52_TEI.xml')
    mscodex75_tei    = os.path.join(os.path.dirname(__file__), 'data/xml/mscodex75_TEI.xml')
    mscodex906_tei   = os.path.join(os.path.dirname(__file__), 'data/xml/mscodex906_TEI.xml')
    mscodex83_tei    = os.path.join(os.path.dirname(__file__), 'data/xml/mscodex83_TEI.xml')


    def setUp(self):
        if not os.path.exists(self.staging_dir):
            os.mkdir(self.staging_dir)

    def tearDown(self):
        if os.path.exists(self.staging_dir):
            shutil.rmtree(self.staging_dir)

    def test_init(self):
        doc = Document.objects.all()[0]
        self.assertIsInstance(Browse(doc.id, outdir=self.staging_dir), Browse)


    def test_browse_page(self):
        Document(base_dir='mscodex52', collection='medren', tei_xml=open(self.mscodex52_tei).read()).save()
        Document(base_dir='mscodex83', collection='medren', tei_xml=open(self.mscodex83_tei).read()).save()
        Document(base_dir='mscodex75', collection='medren', tei_xml=open(self.mscodex75_tei).read()).save()
        for doc in Document.objects.all():
            page = Browse(doc.id, outdir=self.staging_dir)
            page.create_pages()


# Signatures


if __name__ == '__main__':
    unittest.main()
