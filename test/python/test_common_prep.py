#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import shutil
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))
from openn.openn_exception import OPennException
from openn.prep.common_prep import CommonPrep

class TestCommonPrep(unittest.TestCase):

    this_dir         = os.path.dirname(os.path.abspath(__file__))
    staging_dir      = os.path.join(this_dir, 'staging')
    command          = os.path.join(this_dir, '../../bin/op-prep')
    template_dir     = os.path.join(this_dir, '../data/mscodex1223_prepped')
    staged_source    = os.path.join(staging_dir, 'mscodex1223')
    dir_extra_images = os.path.join(this_dir, '../data/mscodex1589_prepped')
    staged_w_extra   = os.path.join(staging_dir, 'mscodex1589')

    def setUp(self):
        if not os.path.exists(TestCommonPrep.staging_dir):
            os.mkdir(TestCommonPrep.staging_dir)

    def tearDown(self):
        if os.path.exists(TestCommonPrep.staging_dir):
           shutil.rmtree(TestCommonPrep.staging_dir)

    def stage_template(self):
        shutil.copytree(TestCommonPrep.template_dir, TestCommonPrep.staged_source)

    def test_run(self):
        # setup
        self.stage_template()
        prep = CommonPrep(TestCommonPrep.staged_source)
        # run
        prep.prep_dir()
    
    def test_no_data_dir(self):
        # setup
        os.mkdir(TestCommonPrep.staged_source)
        # run
        self.assertRaises(OPennException, CommonPrep, TestCommonPrep.staged_source)

if __name__ == '__main__':
    unittest.main()
