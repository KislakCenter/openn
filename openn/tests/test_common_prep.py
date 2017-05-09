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

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))
from openn.openn_exception import OPennException
from openn.prep.common_prep import CommonPrep
from openn.prep.file_list import FileList
from openn.prep.prep_setup import PrepSetup
from openn.prep.prep_config_factory import PrepConfigFactory
from openn.xml.openn_tei import OPennTEI
from openn.models import *
from openn.tests.helpers import *
from openn.tests.openn_test_case import OPennTestCase

class TestCommonPrep(OPennTestCase):

    staging_dir            = os.path.join(os.path.dirname(__file__), 'staging')
    command                = os.path.join(settings.PROJECT_PATH, 'bin/op-prep')
    template_dir           = os.path.join(
        os.path.dirname(__file__), 'data/mscodex1223_prepped')
    staged_source          = os.path.join(staging_dir, 'mscodex1223')
    staged_data            = os.path.join(staged_source, 'data')
    staged_tei             = os.path.join(staged_source, 'PARTIAL_TEI.xml')
    staged_file_list       = os.path.join(staged_source, 'file_list.json')
    dir_extra_images       = os.path.join(
        os.path.dirname(__file__), 'data/mscodex1589_prepped')
    staged_w_extra         = os.path.join(staging_dir, 'mscodex1589')

    prep_cfg_factory       = PrepConfigFactory(
        prep_configs_dict=settings.PREP_CONFIGS,
        prep_methods=settings.PREPARATION_METHODS,
        repository_configs=settings.REPOSITORIES,
        prep_context=settings.PREP_CONTEXT)
    pennpih_prep_config    = prep_cfg_factory.create_prep_config('penn-pih')


    def setUp(self):
        if not os.path.exists(self.staging_dir):
            os.mkdir(self.staging_dir)

    def tearDown(self):
        if os.path.exists(self.staging_dir):
            shutil.rmtree(self.staging_dir)

    def stage_template(self):
        shutil.copytree(self.template_dir, self.staged_source)

    def test_run(self):
        # setup
        self.stage_template()
        repo_wrapper = self.pennpih_prep_config.repository_wrapper()
        doc_count = Document.objects.count()
        doc = PrepSetup().prep_document(repo_wrapper, 'mscodex1223')
        doc_id = doc.id
        prep = CommonPrep(self.staged_source, doc, self.pennpih_prep_config)
        image_count = Image.objects.count()
        deriv_count = Derivative.objects.count()
        # run
        prep.prep_dir()
        self.assertEqual(Document.objects.count(), doc_count + 1)
        self.assertEqual(Image.objects.count(), image_count + prep.package_dir.file_list.file_count)
        self.assertEqual(Derivative.objects.count(), deriv_count + prep.package_dir.file_list.deriv_count)
        doc = Document.objects.get(pk=doc_id)
        self.assertIsNotNone(doc.title)
        self.assertIsNotNone(doc.call_number)

    def test_no_data_dir(self):
        # setup
        os.mkdir(self.staged_source)
        touch(self.staged_tei)
        touch(self.staged_file_list)

        # run
        with self.assertRaises(OPennException) as oe:
            repo_wrapper = self.pennpih_prep_config.repository_wrapper()
            doc = PrepSetup().prep_document(repo_wrapper, 'mscodex1223')
            prep = CommonPrep(self.staged_source, doc, self.pennpih_prep_config)
            prep.prep_dir()
        self.assertIn('data directory', str(oe.exception))

    def test_no_partial_tei(self):
        # setup
        os.mkdir(self.staged_source)
        os.mkdir(self.staged_data)
        touch(self.staged_file_list)

        # run
        with self.assertRaises(OPennException) as oe:
            repo_wrapper = self.pennpih_prep_config.repository_wrapper()
            doc = PrepSetup().prep_document(repo_wrapper, 'mscodex1223')
            prep = CommonPrep(self.staged_source, doc, self.pennpih_prep_config)
            prep.prep_dir()
        self.assertIn('PARTIAL_TEI.xml', str(oe.exception))

    def test_no_file_list(self):
        # setup
        os.mkdir(self.staged_source)
        os.mkdir(self.staged_data)
        touch(self.staged_tei)

        # run
        with self.assertRaises(OPennException) as oe:
            repo_wrapper = self.pennpih_prep_config.repository_wrapper()
            doc = PrepSetup().prep_document(repo_wrapper, 'mscodex1223')
            prep = CommonPrep(self.staged_source, doc, self.pennpih_prep_config)
            prep.prep_dir()
        self.assertIn('file_list.json', str(oe.exception))

    def test_tei_present(self):
        # setup
        self.stage_template()
        repo_wrapper = self.pennpih_prep_config.repository_wrapper()
        doc = PrepSetup().prep_document(repo_wrapper, 'mscodex1223')
        prep = CommonPrep(self.staged_source, doc, self.pennpih_prep_config)

        # run
        self.assertIsInstance(prep.tei, OPennTEI)

    def test_files_present(self):
        # setup
        self.stage_template()
        repo_wrapper = self.pennpih_prep_config.repository_wrapper()
        doc = PrepSetup().prep_document(repo_wrapper, 'mscodex1223')
        prep = CommonPrep(self.staged_source, doc, self.pennpih_prep_config)

        # run
        self.assertIsInstance(prep.files, FileList)

    # TODO: Figure out under what circumstance duplicates should break things
    # def test_duplicate_document(self):
    #     """When a duplicate document is prepped, prep_dir should fail
    #     with an error."""
    #     # setup
    #     self.stage_template()
    #     prep = CommonPrep(self.staged_source, self.medren_coll)
    #     # run
    #     prep.prep_dir()
    #     with self.assertRaises(ValidationError) as ve:
    #         prep.prep_dir()
    #     self.assertIn('already exists', str(ve.exception))

if __name__ == '__main__':
    unittest.main()
