#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import subprocess
import os
import glob
import sys
import re
import shutil

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../lib'))

from openn_exception import OPennException
class TestOpPrep(unittest.TestCase):

    this_dir      = os.path.dirname(os.path.abspath(__file__))
    staging_dir   = os.path.join(this_dir, 'staging')
    command       = os.path.join(this_dir, '../../bin/op-prep')
    template_dir  = os.path.join(this_dir, '../data/mscodex1223')
    staged_source = os.path.join(staging_dir, os.path.basename(template_dir))

    def setUp(self):
        if not os.path.exists(TestOpPrep.staging_dir):
            os.mkdir(TestOpPrep.staging_dir)

    def tearDown(self):
        if os.path.exists(TestOpPrep.staging_dir):
           shutil.rmtree(TestOpPrep.staging_dir)

    def stage_template(self):
        shutil.copytree(TestOpPrep.template_dir, TestOpPrep.staged_source)

    def build_command(self):
        return subprocess.Popen(
                ["python", TestOpPrep.command, TestOpPrep.staged_source],
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


if __name__ == '__main__':
    unittest.main()

