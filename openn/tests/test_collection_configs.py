#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json
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
from openn.collections.configs import Configs
from openn.models import *

class TestCollectionConfigs(TestCase):

    # Paths
    this_dir               = os.path.dirname(__file__)
    collections_dir        = os.path.join(this_dir, 'data/collections')

    # Configuration data
    config_file            = os.path.join(collections_dir, 'collections.json')
    config_data            = json.load(open(config_file))
    valid_collections      = config_data['valid_collections']
    validations            = config_data['validations']
    duplicate_tag          = config_data['duplicate_tag']
    duplicate_name         = config_data['duplicate_name']
    duplicate_include_file = config_data['duplicate_include_file']
    missing_name           = config_data['missing_name']
    missing_tag            = config_data['missing_tag']
    missing_live           = config_data['missing_live']

    def clear_openn_collections_table(self):
        OPennCollection.objects.all().delete()

    def setUp(self):
        pass
        # self.clear_openn_collections_table()

    def tearDown(self):
        pass

    def test_init(self):
        # self.clear_openn_collections_table()
        try:
            configs = Configs(self.valid_collections, self.validations)
        except Exception as ex:
            self.fail("Init should succeed; got error: %s" % (unicode(ex),))

    def test_valid_collections(self):
        # self.clear_openn_collections_table()
        try:
            configs = Configs(self.valid_collections, self.validations)
            configs.validate()
        except OPennException as oe:
            self.fail("Configs for 'valid_collections' should be valid: got error: %s" % (unicode(oe),))

    def test_duplicate_tag(self):
        configs = Configs(self.duplicate_tag, self.validations)
        with self.assertRaises(OPennException) as oe:
            configs.validate()
        self.assertIn('tag', str(oe.exception))

    def test_duplicate_name(self):
        configs = Configs(self.duplicate_name, self.validations)
        with self.assertRaises(OPennException) as oe:
            configs.validate()
        self.assertIn('name', str(oe.exception))

    def test_duplicate_include_file(self):
        configs = Configs(self.duplicate_include_file, self.validations)
        with self.assertRaises(OPennException) as oe:
            configs.validate()
        self.assertIn('include_file', str(oe.exception))
        self.assertIn('2x', str(oe.exception))

    def test_missing_name(self):
        configs = Configs(self.missing_name, self.validations)
        with self.assertRaises(OPennException) as oe:
            configs.validate()
        self.assertRegexpMatches(str(oe.exception), r'\bspace\b')
        self.assertRegexpMatches(str(oe.exception), r'\bempty_string\b')
        self.assertRegexpMatches(str(oe.exception), r'\bno_name\b')
        self.assertRegexpMatches(str(oe.exception), r'\bname\b')

    def test_missing_tag(self):
        configs = Configs(self.missing_tag, self.validations)
        with self.assertRaises(OPennException) as oe:
            configs.validate()
        self.assertRegexpMatches(str(oe.exception), r'\bNOTAG\b')
        self.assertRegexpMatches(str(oe.exception), r'\btag\b')

    def test_missing_live(self):
        configs = Configs(self.missing_live, self.validations)
        with self.assertRaises(OPennException) as oe:
            configs.validate()
        self.assertRegexpMatches(str(oe.exception), r'\blive\b')
        self.assertRegexpMatches(str(oe.exception), r'\bfriendshl\b')
