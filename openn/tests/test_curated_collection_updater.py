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
from openn.curated.updater import Updater
from openn.models import *
from openn.tests.openn_test_case import OPennTestCase

class TestCuratedCollectionUpdater(OPennTestCase):

    # Paths
    this_dir               = os.path.dirname(__file__)
    curated_dir            = os.path.join(this_dir, 'data/curated')

    # Configuration data
    config_file            = os.path.join(curated_dir, 'configs.json')
    config_data            = json.load(open(config_file))

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_init(self):
        try:
            updater = Updater(self.config_data['configs'])
        except Exception as ex:
            self.fail("Init should succeed; got error: %s" % (unicode(ex),))

    def test_update_all(self):
        updater = Updater(self.config_data['configs'])
        try:
            updater.update_all()
        except Exception as ex:
            self.fail("Update all should succeed; got error: %s" % (unicode(ex),))
        self.assertGreater(CuratedCollection.objects.count(), 0)

    def test_config_changes(self):
        first_config = deepcopy(self.config_data['configs'][0])

        # create the CuratedCollection in the databaase
        updater = Updater(self.config_data['configs'])
        updater.update(first_config)
        self.assertEqual(CuratedCollection.objects.count(), 1)

        # now change the config
        first_config['name'] = 'New name'
        updater.update(first_config)
        curated = CuratedCollection.objects.get(tag = first_config['tag'])
        self.assertEqual(curated.name, 'New name')
