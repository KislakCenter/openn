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
from openn.project.updater import Updater
from openn.models import *

class TestProjectUpdater(TestCase):

    # Paths
    this_dir               = os.path.dirname(__file__)
    projects_dir           = os.path.join(this_dir, 'data/projects')

    # Configuration data
    config_file            = os.path.join(projects_dir, 'configs.json')
    config_data            = json.load(open(config_file))

    # def clear_openn_collections_table(self):
    #     OPennCollection.objects.all().delete()

    def setUp(self):
        pass
        # self.clear_openn_collections_table()

    def tearDown(self):
        pass

    def test_init(self):
        # self.clear_openn_collections_table()
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
        self.assertGreater(Project.objects.count(), 0)

    def test_config_changes(self):
        first_config = deepcopy(self.config_data['configs'][0])

        # create the Project in the databaase
        updater = Updater(self.config_data['configs'])
        updater.update(first_config)
        self.assertEqual(Project.objects.count(), 1)

        # now change the config
        first_config['name'] = 'New name'
        updater.update(first_config)
        project = Project.objects.get(tag = first_config['tag'])
        self.assertEqual(project.name, 'New name')
