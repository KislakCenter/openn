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
from openn.prep.prep_config_factory import PrepConfigFactory
from openn.models import *
from openn.tests.openn_test_case import OPennTestCase

class TestMedrenPrep(OPennTestCase):

    staging_dir      = os.path.join(os.path.dirname(__file__), 'staging')
    # template_dir     = os.path.join(os.path.dirname(__file__), 'data/mscodex1589')
    # staged_source    = os.path.join(staging_dir, 'mscodex1589')
    template_dir     = os.path.join(os.path.dirname(__file__), 'data/mscodex1223')
    staged_source    = os.path.join(staging_dir, 'mscodex1223')
    prep_cfg_factory = PrepConfigFactory(
        prep_configs_dict=settings.PREP_CONFIGS,
        prep_methods=settings.PREPARATION_METHODS,
        repository_configs=settings.REPOSITORIES,
        prep_context=settings.PREP_CONTEXT)
    pennpih_prep_config = prep_cfg_factory.create_prep_config('penn-pih')
    complex_files    = os.path.join(os.path.dirname(__file__), 'data/ljs472')
    complex_pih_src  = os.path.join(os.path.dirname(__file__), 'data/xml/ljs472.xml')
    complex_staged   = os.path.join(staging_dir, 'ljs472')
    complex_pih_xml  = os.path.join(complex_staged, 'pih.xml')
    ljs_prep_config = prep_cfg_factory.create_prep_config('ljs-pih')
    pp               = PrettyPrinter(indent=2)

    def setUp(self):
        if not os.path.exists(self.staging_dir):
            os.mkdir(self.staging_dir)

    def tearDown(self):
        if os.path.exists(self.staging_dir):
            shutil.rmtree(self.staging_dir)

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
        self.pp.pprint(thing)

    def stage_template(self):
        shutil.copytree(self.template_dir, self.staged_source)

    def test_run(self):
        # setup
        self.stage_template()
        doc_count = Document.objects.count()
        repo_wrapper = self.pennpih_prep_config.repository_wrapper()
        doc = PrepSetup().prep_document(repo_wrapper, 'mscodex1223')
        prep = MedrenPrep(source_dir=self.staged_source, document=doc,
                          prep_config = self.pennpih_prep_config)
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
        shutil.copytree(self.complex_files, self.complex_staged)
        repo_wrapper = self.ljs_prep_config.repository_wrapper()
        doc = PrepSetup().prep_document(repo_wrapper, 'ljs472')
        prep = MedrenPrep(self.complex_staged, doc, self.ljs_prep_config)
        files = prep.build_file_list(self.complex_pih_xml)
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
