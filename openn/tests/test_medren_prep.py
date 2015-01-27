#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import shutil
import sys
import glob
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
    # template_dir     = os.path.join(os.path.dirname(__file__), 'data/mscodex1589')
    # staged_source    = os.path.join(staging_dir, 'mscodex1589')
    template_dir     = os.path.join(os.path.dirname(__file__), 'data/mscodex1223')
    staged_source    = os.path.join(staging_dir, 'mscodex1223')
    medren_coll      = 'medren'
    complex_files    = os.path.join(os.path.dirname(__file__), 'data/ljs472')
    complex_pih_src  = os.path.join(os.path.dirname(__file__), 'data/xml/ljs472.xml')
    complex_staged   = os.path.join(staging_dir, 'ljs472')
    complex_pih_xml  = os.path.join(complex_staged, 'pih.xml')
    ljs_coll         = 'ljs'
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

    def assertHasFile(self,file_list, group, path):
        for info in file_list[group]:
            if info['filename'] == path:
                return True
        raise AssertionError("Expected file: '%s' in group: '%s'" % (path,group))

    def assertNotHasFile(self,file_list, group, path):
        for info in file_list[group]:
            if info['filename'] == path:
                raise AssertionError("Should not have file: '%s' in group: '%s'" % (path,group))

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
        # run
        prep.prep_dir()

    # ljs472_wk1_back0002a.tif    # not used by PIH
    # ljs472_wk1_back0002b.tif    # not used by PIH
    # ljs472_wk1_body0065a.tif    # extra file; listed in PIH
    # ljs472_wk1_body0065b.tif    # extra file; listed in PIH
    # ljs472_wk1_body0193.tif     # 'blank' file not in PIH
    # ljs472_wk1_body0194.tif     # 'blank' file not in PIH
    # ljs472_wk1_body0195.tif     # 'blank' file not in PIH
    # ljs472_wk1_body0196.tif     # 'blank' file not in PIH
    def test_complex_names(self):
        # setup
        shutil.copytree(TestMedrenPrep.complex_files, TestMedrenPrep.complex_staged)
        doc = PrepSetup().prep_document(TestMedrenPrep.ljs_coll, 'ljs472')
        prep = MedrenPrep(TestMedrenPrep.complex_staged, TestMedrenPrep.ljs_coll, doc)
        files = prep.build_file_list(TestMedrenPrep.complex_pih_xml)
        self.assertHasFile(files, 'document', 'data/ljs472_wk1_body0193.tif')
        self.assertHasFile(files, 'document', 'data/ljs472_wk1_body0194.tif')
        self.assertHasFile(files, 'document', 'data/ljs472_wk1_body0195.tif')
        self.assertHasFile(files, 'document', 'data/ljs472_wk1_body0196.tif')
        self.assertHasFile(files, 'document', 'data/ljs472_wk1_body0065a.tif')
        self.assertHasFile(files, 'document', 'data/ljs472_wk1_body0065b.tif')
        self.assertHasFile(files, 'extra', 'data/ljs472_wk1_back0002a.tif')
        self.assertHasFile(files, 'extra', 'data/ljs472_wk1_back0002a.tif')
        self.assertNotHasFile(files, 'extra', 'data/ljs472_wk1_body0193.tif')
        self.assertNotHasFile(files, 'extra', 'data/ljs472_wk1_body0194.tif')
        self.assertNotHasFile(files, 'extra', 'data/ljs472_wk1_body0195.tif')
        self.assertNotHasFile(files, 'extra', 'data/ljs472_wk1_body0196.tif')
        self.assertNotHasFile(files, 'extra', 'data/ljs472_wk1_body0065a.tif')
        self.assertNotHasFile(files, 'extra', 'data/ljs472_wk1_body0065b.tif')
        self.assertNotHasFile(files, 'document', 'data/ljs472_wk1_back0002a.tif')
        self.assertNotHasFile(files, 'document', 'data/ljs472_wk1_back0002a.tif')

if __name__ == '__main__':
    unittest.main()
