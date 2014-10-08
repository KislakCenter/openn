#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.core.cache import cache
from django.core.urlresolvers import reverse
from django.db import transaction
from django.db.models import Avg, Count, F, Max, Min, Sum, Q
from django.utils import timezone
from django.utils import unittest
from django.test import TestCase
from django.conf import settings
from django import db
from django.db import models
from openn.models import *
from openn.pages.table_of_contents import TableOfContents
from openn.pages.browse import Browse
import subprocess
import json
import os
import glob
import sys
import re
import shutil

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from openn.openn_exception import OPennException
class TestOpGenPages(TestCase):

    fixtures = [ 'test.json' ]

    staging_dir      = os.path.join(os.path.dirname(__file__), 'staging')
    images_dir       = os.path.join(staging_dir, 'images')
    data_staging     = settings.STAGING_DIR
    command          = os.path.join(settings.PROJECT_PATH, 'bin/op-gen-pages')
    template_dir     = os.path.join(os.path.dirname(__file__), 'data/mscodex1223_prepped')
    db_file          = os.path.join(settings.PROJECT_PATH, 'openn/tests/database.sqlite3')
    staged_images    = os.path.join(images_dir, 'mscodex1223')

    def setUp(self):
        dirs  = [
            TestOpGenPages.staging_dir,
            TestOpGenPages.images_dir,
            TestOpGenPages.data_staging
        ]
        for d in dirs:
            if not os.path.exists(d):
                os.mkdir(d)

    def tearDown(self):
        # have to delete the stuff from the database
        for m in models.get_models():
            table = m._meta.db_table
            self.empty_table(table)
        # if os.path.exists(TestOpGenPages.staging_dir):
        #     shutil.rmtree(TestOpGenPages.staging_dir)

    def empty_table(self, table):
        p = subprocess.Popen(['sqlite3', TestOpGenPages.db_file, ('delete from %s' % table )])
        p.communicate()

    def stage_template(self):
        shutil.copytree(TestOpGenPages.template_dir, TestOpGenPages.staged_source)

    def build_command(self,dir=None):
        return subprocess.Popen(
                ["python", TestOpGenPages.command ],
                stderr=subprocess.PIPE,
                stdout=subprocess.PIPE)

    def test_run(self):
        p = self.build_command()
        out, err = p.communicate()
        self.assertEqual(0, p.returncode, err)

    def test_table_of_contents(self):
        pages = TableOfContents('medren', **{
            'template_name': 'TableOfContents.html',
            'outdir': settings.STAGING_DIR
            })
        pages.create_pages()

    def test_browse(self):
        pages = Browse(1, 'medren',
                       **{ 'template_name': 'browse_ms.html',
                           'outdir': settings.STAGING_DIR })
        pages.create_pages()

if __name__ == '__main__':
    unittest.main()
