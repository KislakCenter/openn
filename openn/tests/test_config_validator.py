#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json
import sys

from copy import deepcopy

from django.utils import unittest
from django.test import TestCase
from django.conf import settings
from django.core.exceptions import ValidationError
from pprint import PrettyPrinter

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))
from openn.openn_exception import OPennException
from openn.repository.config_validator import ConfigValidator
from openn.models import *
from openn.tests.openn_test_case import OPennTestCase

class TestConfigValidator(OPennTestCase):

    # Paths
    this_dir               = os.path.dirname(__file__)
    curated_dir           = os.path.join(this_dir, 'data/curated')

    # Configuration data
    config_file            = os.path.join(curated_dir, 'configs.json')
    config_data            = json.load(open(config_file))
    configs_dict           = config_data['configs']
    validator_dict         = config_data['validations']
    missing_tag            = config_data['missing_tag']
    missing_name           = config_data['missing_name']
    duplicate_tag          = config_data['duplicate_tag']
    duplicate_name         = config_data['duplicate_name']


    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_init(self):
        try:
            validator = ConfigValidator(self.validator_dict, self.configs_dict)
        except Exception as ex:
            self.fail("Init should succeed; got error: %s" % (unicode(ex),))

    def test_validate(self):
        validator = ConfigValidator(self.validator_dict, self.configs_dict)
        try:
            validator.validate()
        except Exception as ex:
            self.fail(
                "Validate should succeed; got error: %s" % (unicode(ex),))

    def test_duplicate_tag(self):
        validator = ConfigValidator(self.validator_dict, self.duplicate_tag)
        with self.assertRaises(OPennException) as oe:
            validator.validate()
        self.assertIn('tag', str(oe.exception))

    def test_duplicate_name(self):
        validator = ConfigValidator(self.validator_dict, self.duplicate_name)
        with self.assertRaises(OPennException) as oe:
            validator.validate()
        self.assertIn('name', str(oe.exception))

    def test_missing_tag(self):
        validator = ConfigValidator(self.validator_dict, self.missing_tag)
        with self.assertRaises(OPennException) as oe:
            validator.validate()
        self.assertIn('tag', str(oe.exception))

    def test_missing_name(self):
        validator = ConfigValidator(self.validator_dict, self.missing_name)
        with self.assertRaises(OPennException) as oe:
            validator.validate()
        self.assertIn('name', str(oe.exception))