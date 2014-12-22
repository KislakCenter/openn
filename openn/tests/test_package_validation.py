#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import shutil
import sys
import glob
from pprint import PrettyPrinter
from django.utils import unittest
from django.test import TestCase
from django.conf import settings
from django.core.exceptions import ValidationError

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))
from openn.openn_exception import OPennException
from openn.prep.package_validation import PackageValidation
from openn.models import *

class TestPackageValidation(TestCase):
    pass

    pp                = PrettyPrinter(indent=2)
    staging_dir       = os.path.join(os.path.dirname(__file__), 'staging')
    template_dir      = os.path.join(os.path.dirname(__file__), 'data/package_validation')
    staged_package    = os.path.join(staging_dir, 'package_validation')
    validation_config = {
        'valid_names': ['*.tif', 'bibid.txt'],
        'invalid_names': ['CaptureOne', 'Output', '*[()]*'],
        'required_names': ['*.tif', 'bibid.txt']
    }

    def touch(self,fname):
        with open(fname, 'a'):
            os.utime(fname, None)

    def setUp(self):
        if not os.path.exists(TestPackageValidation.staging_dir):
            os.mkdir(TestPackageValidation.staging_dir)

    def tearDown(self):
        if os.path.exists(TestPackageValidation.staging_dir):
            shutil.rmtree(TestPackageValidation.staging_dir)

    def stage_template(self):
        shutil.copytree(TestPackageValidation.template_dir, TestPackageValidation.staged_package)

    def test_run(self):
        # setup
        self.stage_template()
        validation = PackageValidation(**TestPackageValidation.validation_config)
        # run
        errors = validation.validate(TestPackageValidation.staged_package)
        self.assertTrue(len(errors) == 0)

    def test_invalid_dir(self):
        self.stage_template()
        os.mkdir(os.path.join(self.staged_package, 'CaptureOne'))
        validation = PackageValidation(**TestPackageValidation.validation_config)
        # run
        errors = validation.validate(TestPackageValidation.staged_package)
        self.assertTrue(len(errors) > 0)
        self.assertIn('CaptureOne', validation.check_invalid_names(TestPackageValidation.staged_package))

    def test_invalid_valid_file(self):
        # test a file that passes the check_valid_names test '\.tif$', but fails the
        # check_invalid_names test '[()]'
        self.stage_template()
        self.touch(os.path.join(self.staged_package, 'somefile(1).tif'))
        validation = PackageValidation(**self.validation_config)
        # run
        errors = validation.validate(self.staged_package)
        self.assertTrue(len(errors) > 0)
        errors = validation.check_invalid_names(TestPackageValidation.staged_package)
        self.assertIn('somefile(1).tif', errors)

    def test_missing_required(self):
        self.stage_template()
        os.remove(os.path.join(self.staged_package, 'bibid.txt'))
        validation = PackageValidation(**self.validation_config)
        # run
        errors = validation.validate(self.staged_package)
        self.assertTrue(len(errors) > 0)
        errors = validation.check_required(TestPackageValidation.staged_package)
        self.assertIn('bibid.txt', errors)



if __name__ == '__main__':
    unittest.main()
