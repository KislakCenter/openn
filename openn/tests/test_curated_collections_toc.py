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
from openn.pages.curated_collection_toc import CuratedCollectionTOC
from openn.models import CuratedCollection
from openn.tests.openn_test_case import OPennTestCase

from openn.tests.helpers import *

# import logging
# logger = logging.getLogger()
# logger.setLevel(logging.DEBUG)

class TestCuratedCollectionsTOC(OPennTestCase):
    fixtures = ['test.json']

    staging_dir = os.path.join(os.path.dirname(__file__), 'staging')

    TEST_INCLUDE_FILE = 'TestCuratedCollectionIncludeFile.html'
    TEST_INCLUDE_FILE_PATH = os.path.join(
        settings.SITE_ROOT, 'templates', TEST_INCLUDE_FILE)
    TEST_TEMPLATE = 'TestCuratedCollection.html'
    TEST_TEMPLATE_PATH = os.path.join(
        settings.SITE_ROOT, 'templates', TEST_TEMPLATE)

    TEST_CURATED_COLLECTION = {
        'tag': 'test',
        'name': 'Test Manuscripts',
        'blurb': 'Lorem ipsum',
        'include_file': TEST_INCLUDE_FILE,
        'csv_only': False,
        'live': True,
    }

    _original_log_handler = None

    def setup_test_collection(self):
        touch(self.TEST_TEMPLATE_PATH)
        touch(self.TEST_INCLUDE_FILE_PATH)
        return CuratedCollection(**self.TEST_CURATED_COLLECTION).save()

    @staticmethod
    def alter_file(file_path):
        os.system("echo 'Hi.' >> %s " % file_path)

    def touch_test_template(self):
        touch(self.TEST_TEMPLATE_PATH)

    # @classmethod
    # def setUpClass(cls):
    #     super(TestCuratedCollectionsTOC, cls).setUpClass()
    #     # Assuming you follow Python's logging module's documentation's
    #     # recommendation about naming your module's logs after the module's
    #     # __name__,the following getLogger call should fetch the same logger
    #     # you use in the foo module
    #     log = logging.getLogger()
    #     # TestCuratedCollectionsTOC._original_log_handler = cls._log_handler
    #     cls._log_handler = MockLoggingHandler(level='DEBUG')
    #     log.addHandler(cls._log_handler)
    #     # cls.log_messages = cls._log_handler.messages
    #     cls.log_messages = cls._log_handler.messages

    def setUp(self):
        super(TestCuratedCollectionsTOC, self).setUp()
        self._log_handler.reset()
        if os.path.exists(self.staging_dir):
            shutil.rmtree(self.staging_dir)
        if not os.path.exists(self.staging_dir):
            os.mkdir(self.staging_dir)

    def tearDown(self):
        if os.path.exists(self.staging_dir):
            shutil.rmtree(self.staging_dir)
        for templ in [self.TEST_TEMPLATE_PATH, self.TEST_INCLUDE_FILE_PATH]:
            if os.path.exists(templ):
                os.remove(templ)

    def test_init(self):
        self.setup_test_collection()
        page = CuratedCollectionTOC(
            curated_tag='test',
            toc_dir=settings.TOC_DIR,
            template_name=self.TEST_TEMPLATE,
            outdir=self.staging_dir)
        self.assertIsInstance(page, CuratedCollectionTOC)

    def test_is_needed(self):
        self.setup_test_collection()
        add_to_curated('test')
        page = CuratedCollectionTOC(
            curated_tag='test',
            toc_dir=settings.TOC_DIR,
            template_name=self.TEST_TEMPLATE,
            outdir=self.staging_dir)
        page.is_needed()

        self.assertIn(
            'Curated collection HTML file does not exist',
            format_logging(self.log_messages))

    def test_template_has_changed(self):
        self.setup_test_collection()
        add_to_curated('test')
        page = CuratedCollectionTOC(
            curated_tag='test',
            toc_dir=settings.TOC_DIR,
            template_name=self.TEST_TEMPLATE,
            outdir=self.staging_dir)
        page.create_pages()
        self.reset_log_handler()
        self.alter_file(self.TEST_TEMPLATE_PATH)
        page.is_needed()

        self.assertIn(
            'Curated collection template file has changed',
            format_logging(self.log_messages))

    def test_include_file_has_changed(self):
        self.setup_test_collection()
        add_to_curated('test')
        page = CuratedCollectionTOC(
            curated_tag='test',
            toc_dir=settings.TOC_DIR,
            template_name=self.TEST_TEMPLATE,
            outdir=self.staging_dir)
        page.create_pages()
        self.reset_log_handler()
        self.alter_file(self.TEST_INCLUDE_FILE_PATH)
        page.is_needed()

        self.assertIn(
            'Curated collection include file has changed',
            format_logging(self.log_messages))

    def test_no_last_generated_date(self):
        self.setup_test_collection()
        add_to_curated('test')
        page = CuratedCollectionTOC(
            curated_tag='test',
            toc_dir=settings.TOC_DIR,
            template_name=self.TEST_TEMPLATE,
            outdir=self.staging_dir)
        page.set_site_file()
        page.site_file.update_template_sha256()
        page.site_file.update_include_file_sha256()
        ensure_file(page.outfile_path())
        page.is_needed()

        self.assertIn(
            'Curated collection HTML has no last generated date; generating',
            format_logging(self.log_messages))

    def test_no_change_since_generated(self):
        self.setup_test_collection()
        add_to_curated('test')
        page = CuratedCollectionTOC(
            curated_tag='test',
            toc_dir=settings.TOC_DIR,
            template_name=self.TEST_TEMPLATE,
            outdir=self.staging_dir)
        page.create_pages()
        self.reset_log_handler()
        page.is_needed()

        self.assertIn(
            "object hasn't changed since Curated collection HTML last generated",
            format_logging(self.log_messages))


if __name__ == '__main__':
    unittest.main()
