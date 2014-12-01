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
from openn.prep.common_prep import CommonPrep
from openn.prep.file_list import FileList
from openn.prep.prep_setup import PrepSetup
from openn.xml.openn_tei import OPennTEI
from openn.models import *

class TestCommonPrep(TestCase):

    staging_dir      = os.path.join(os.path.dirname(__file__), 'staging')
    command          = os.path.join(settings.PROJECT_PATH, 'bin/op-prep')
    template_dir     = os.path.join(os.path.dirname(__file__), 'data/mscodex1223_prepped')
    staged_source    = os.path.join(staging_dir, 'mscodex1223')
    staged_data      = os.path.join(staged_source, 'data')
    staged_tei       = os.path.join(staged_source, 'PARTIAL_TEI.xml')
    staged_file_list = os.path.join(staged_source, 'file_list.json')
    dir_extra_images = os.path.join(os.path.dirname(__file__), 'data/mscodex1589_prepped')
    staged_w_extra   = os.path.join(staging_dir, 'mscodex1589')
    medren_coll      = 'medren'
    pp               = PrettyPrinter(indent=2)

    def setUp(self):
        if not os.path.exists(TestCommonPrep.staging_dir):
            os.mkdir(TestCommonPrep.staging_dir)

    def tearDown(self):
        if os.path.exists(TestCommonPrep.staging_dir):
            shutil.rmtree(TestCommonPrep.staging_dir)

    def touch(self, filename, times=None):
        with(open(filename,'a')):
            os.utime(filename, times)

    def pprint(self,thing):
        TestCommonPrep.pp.pprint(thing)

    def stage_template(self):
        shutil.copytree(TestCommonPrep.template_dir, TestCommonPrep.staged_source)

    def test_run(self):
        # setup
        self.stage_template()
        doc_count = Document.objects.count()
        doc = PrepSetup().prep_document(TestCommonPrep.medren_coll, 'mscodex1223')
        prep = CommonPrep(TestCommonPrep.staged_source, TestCommonPrep.medren_coll, doc)
        image_count = Image.objects.count()
        deriv_count = Derivative.objects.count()
        # run
        prep.prep_dir()
        self.assertEqual(Document.objects.count(), doc_count + 1)
        self.assertEqual(Image.objects.count(), image_count + prep.package_dir.file_list.file_count)
        self.assertEqual(Derivative.objects.count(), deriv_count + prep.package_dir.file_list.deriv_count)

    def test_no_data_dir(self):
        # setup
        os.mkdir(TestCommonPrep.staged_source)
        self.touch(TestCommonPrep.staged_tei)
        self.touch(TestCommonPrep.staged_file_list)

        # run
        with self.assertRaises(OPennException) as oe:
            doc = PrepSetup().prep_document(TestCommonPrep.medren_coll, 'mscodex1223')
            CommonPrep(TestCommonPrep.staged_source, TestCommonPrep.medren_coll, doc)
        self.assertIn('data directory', str(oe.exception))

    def test_no_partial_tei(self):
        # setup
        os.mkdir(TestCommonPrep.staged_source)
        os.mkdir(TestCommonPrep.staged_data)
        self.touch(TestCommonPrep.staged_file_list)

        # run
        with self.assertRaises(OPennException) as oe:
            doc = PrepSetup().prep_document(TestCommonPrep.medren_coll, 'mscodex1223')
            CommonPrep(TestCommonPrep.staged_source, TestCommonPrep.medren_coll, doc)
        self.assertIn('PARTIAL_TEI.xml', str(oe.exception))

    def test_no_file_list(self):
        # setup
        os.mkdir(TestCommonPrep.staged_source)
        os.mkdir(TestCommonPrep.staged_data)
        self.touch(TestCommonPrep.staged_tei)

        # run
        with self.assertRaises(OPennException) as oe:
            doc = PrepSetup().prep_document(TestCommonPrep.medren_coll, 'mscodex1223')
            CommonPrep(TestCommonPrep.staged_source, TestCommonPrep.medren_coll, doc)
        self.assertIn('file_list.json', str(oe.exception))

    def test_tei_present(self):
        # setup
        self.stage_template()
        doc = PrepSetup().prep_document(TestCommonPrep.medren_coll, 'mscodex1223')
        prep = CommonPrep(TestCommonPrep.staged_source, TestCommonPrep.medren_coll, doc)

        # run
        self.assertIsInstance(prep.tei, OPennTEI)

    def test_files_present(self):
        # setup
        self.stage_template()
        doc = PrepSetup().prep_document(TestCommonPrep.medren_coll, 'mscodex1223')
        prep = CommonPrep(TestCommonPrep.staged_source, TestCommonPrep.medren_coll, doc)

        # run
        self.assertIsInstance(prep.files, FileList)

    def test_collection_empty(self):
        """ if the test collection is the empty string, the prep should fail when
        it tries to create the CommonPrep instance.
        """
        # setup
        self.stage_template()
        with self.assertRaises(OPennException) as oe:
            doc = PrepSetup().prep_document(TestCommonPrep.medren_coll, 'mscodex1223')
            prep = CommonPrep(TestCommonPrep.staged_source, '', doc)
        self.assertIn('collection', str(oe.exception))

    # TODO: Figure out under what circumstance duplicates should break things
    # def test_duplicate_document(self):
    #     """When a duplicate document is prepped, prep_dir should fail
    #     with an error."""
    #     # setup
    #     self.stage_template()
    #     prep = CommonPrep(TestCommonPrep.staged_source, TestCommonPrep.medren_coll)
    #     # run
    #     prep.prep_dir()
    #     with self.assertRaises(ValidationError) as ve:
    #         prep.prep_dir()
    #     self.assertIn('already exists', str(ve.exception))

if __name__ == '__main__':
    unittest.main()
