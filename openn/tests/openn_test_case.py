#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.utils import unittest
from django.test import TestCase

from openn.tests.helpers import *

import logging
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

class OPennTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        super(OPennTestCase, cls).setUpClass()
        # Assuming you follow Python's logging module's documentation's
        # recommendation about naming your module's logs after the module's
        # __name__,the following getLogger call should fetch the same logger
        # you use in the foo module
        log = logging.getLogger()
        # TestCuratedCollectionsTOC._original_log_handler = cls._log_handler
        cls._log_handler = MockLoggingHandler(level='DEBUG')
        log.addHandler(cls._log_handler)
        # cls.log_messages = cls._log_handler.messages
        cls.log_messages = cls._log_handler.messages


    def reset_log_handler(self):
        self._log_handler.reset()