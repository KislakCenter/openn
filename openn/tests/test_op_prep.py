#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.utils import unittest
from django.test import TestCase
from django.conf import settings
import subprocess
import json
import os
import glob
import sys
import re
import shutil

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from openn.openn_exception import OPennException
class TestOpPrep(TestCase):

    staging_dir   = os.path.join(settings.PROJECT_PATH, 'test/staging')
    command       = os.path.join(settings.PROJECT_PATH, 'bin/op-prep')
    template_dir  = os.path.join(settings.PROJECT_PATH, 'test/data/mscodex1223')
    staged_source = os.path.join(staging_dir, os.path.basename(template_dir))
    partial_tei   = os.path.join(staged_source, 'PARTIAL_TEI.xml')
    file_list     = os.path.join(staged_source, 'file_list.json')
    prep_config   = 'medren'
    dir_extra_images = os.path.join(settings.PROJECT_PATH, 'test/data/mscodex1589')
    staged_w_extra   = os.path.join(staging_dir, os.path.basename(dir_extra_images))

    def setUp(self):
        if not os.path.exists(TestOpPrep.staging_dir):
            os.mkdir(TestOpPrep.staging_dir)

    def tearDown(self):
        if os.path.exists(TestOpPrep.staging_dir):
           shutil.rmtree(TestOpPrep.staging_dir)

    def stage_template(self):
        shutil.copytree(TestOpPrep.template_dir, TestOpPrep.staged_source)

    def build_command(self,dir=None):
        dir = dir or TestOpPrep.staged_source
        return subprocess.Popen(
                ["python", TestOpPrep.command, TestOpPrep.prep_config, dir],
                stderr=subprocess.PIPE,
                stdout=subprocess.PIPE)

    def test_run(self):
        # setup
        self.stage_template()
        # run
        p = self.build_command()
        out, err = p.communicate()
        # test
        self.assertEqual(0, p.returncode, err)
        self.assertTrue(os.path.exists(TestOpPrep.partial_tei),
                "Expected TEI file: %s" % TestOpPrep.partial_tei)
        self.assertTrue(os.path.exists(TestOpPrep.file_list),
                "Expected TEI file: %s" % TestOpPrep.file_list)

    def test_images_not_in_pih(self):
        # setup
        shutil.copytree(TestOpPrep.dir_extra_images, TestOpPrep.staged_w_extra)
        # run
        p = self.build_command(TestOpPrep.staged_w_extra)
        out, err = p.communicate()
        # test
        self.assertEqual(0, p.returncode, err)
        file_list = os.path.join(TestOpPrep.staged_w_extra, 'file_list.json')
        self.assertTrue(os.path.exists(file_list), 
                "Expected TEI file: %s" % file_list)

    def test_bad_source_dir(self):
        # run
        p = self.build_command()
        out, err = p.communicate()
        self.assertNotEqual(0, p.returncode, "Exit code should not be 0")
        self.assertTrue(re.search("Could not find source_dir", err) is not None)

    def test_no_bibidtxt(self):
        # setup
        os.mkdir(TestOpPrep.staged_source)
        # run
        p = self.build_command()
        # test
        out, err = p.communicate()
        self.assertNotEqual(0, p.returncode, "Exit code should not be 0")
        self.assertTrue(re.search("Could not find bibid.txt", err) is not None)

    def test_bad_bibid(self):
        # setup
        os.mkdir(TestOpPrep.staged_source)
        # create a bad bibid value
        bibid = open(os.path.join(TestOpPrep.staged_source, 'bibid.txt'), 'w')
        bibid.write('1234x')
        bibid.close()
        # run
        p = self.build_command()
        out, err = p.communicate()
        # test
        self.assertNotEqual(0, p.returncode, "Exit code should not be 0")
        self.assertTrue(re.search("Bad BibID.*'1234x'", err) is not None)

    def test_missing_files(self):
        # setup
        self.stage_template()
        tiff = glob.glob(os.path.join(TestOpPrep.staged_source, '*.tif'))[-1]
        os.remove(tiff)
        # run
        p = self.build_command()
        out, err = p.communicate()
        # test
        self.assertNotEqual(0, p.returncode, "Exit code should not be 0")
        self.assertTrue(re.search("Expected images", err) is not None)

    def test_no_call_num(self):
        # setup
        os.mkdir(TestOpPrep.staged_source)
        bibid = open(os.path.join(TestOpPrep.staged_source, 'bibid.txt'), 'w')
        bibid.write('9999999999')
        bibid.close()
        # run
        p = self.build_command()
        out, err = p.communicate()
        # test
        self.assertNotEqual(0, p.returncode, "Exit code should not be 0")
        self.assertTrue(re.search("No call number.*9999999999", err) is not None)

    def test_bad_collection_name(self):
        # setup
        # run
        p = subprocess.Popen(
                ["python", TestOpPrep.command, 'bad_collection', TestOpPrep.staged_source],
                stderr=subprocess.PIPE,
                stdout=subprocess.PIPE)
        out, err = p.communicate()
        # test
        self.assertNotEqual(0, p.returncode, "Exit code should not be 0")
        self.assertTrue(re.search("Configuration not found", err) is not None)

        

if __name__ == '__main__':
    unittest.main()

