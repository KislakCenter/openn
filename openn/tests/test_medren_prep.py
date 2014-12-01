#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import shutil
import sys
from django.utils import unittest
from django.test import TestCase
from django.conf import settings
from django.core.exceptions import ValidationError
from pprint import PrettyPrinter

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))
from openn.openn_exception import OPennException
from openn.prep.medren_prep import MedrenPrep
from openn.prep.file_list import FileList
from openn.xml.openn_tei import OPennTEI
from openn.prep.prep_setup import PrepSetup
from openn.models import *

class TestMedrenPrep(TestCase):

    staging_dir      = os.path.join(os.path.dirname(__file__), 'staging')
    template_dir     = os.path.join(os.path.dirname(__file__), 'data/mscodex1223')
    staged_source    = os.path.join(staging_dir, 'mscodex1223')
    medren_coll      = 'medren'
    pp               = PrettyPrinter(indent=2)

    def setUp(self):
        if not os.path.exists(TestMedrenPrep.staging_dir):
            os.mkdir(TestMedrenPrep.staging_dir)

    def tearDown(self):
        if os.path.exists(TestMedrenPrep.staging_dir):
            shutil.rmtree(TestMedrenPrep.staging_dir)

    def touch(self, filename, times=None):
        with(open(filename,'a')):
            os.utime(filename, times)

    def pprint(self,thing):
        TestMedrenPrep.pp.pprint(thing)

    def stage_template(self):
        shutil.copytree(TestMedrenPrep.template_dir, TestMedrenPrep.staged_source)

    def test_run(self):
        # setup
        self.stage_template()
        doc_count = Document.objects.count()
        doc = PrepSetup().prep_document(TestMedrenPrep.medren_coll, 'mscodex1223')
        prep = MedrenPrep(TestMedrenPrep.staged_source, TestMedrenPrep.medren_coll, doc)
        image_count = Image.objects.count()
        deriv_count = Derivative.objects.count()
        # run
        prep.prep_dir()

if __name__ == '__main__':
    unittest.main()
