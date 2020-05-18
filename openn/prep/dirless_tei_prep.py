# -*- coding: utf-8 -*-
import os
import re
import logging
import sys

sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))
from openn.openn_exception import OPennException
from openn.openn_functions import *
from openn.xml.openn_tei import OPennTEI
from openn.prep.prep_setup import PrepSetup

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "openn.settings")
from openn.models import *
from openn import openn_db
from django.core import serializers
from django.conf import settings

class DirlessTEIPrep(object):

    logger = logging.getLogger(__name__)

    def __init__(self, source_dir, doc, prep_config):
        """Create a new TEI for the given PrepConfig 'prep_config',
        'folder_name', and 'tei_file'.
        """
        self.source_dir = source_dir
        self._doc       = doc
        self._tei_file  = os.path.join(self.source_dir, 'TEI.xml')

    def validate(self):
        self._validate_tei()

    def prep_dir(self):
        self.validate()

        # set up the document
        self._doc.tei_xml = self._read_tei()
        openn_tei = self._openn_tei()
        self._doc.title = openn_tei.title
        self._doc.call_number = openn_tei.call_number
        self._doc.save()

    def _read_tei(self):
        return open(self._tei_file).read()

    def _openn_tei(self):
        return OPennTEI(self._read_tei())

    def _validate_tei(self):
        # Confirm the TEI file exists
        if not os.path.exists(self._tei_file):
            raise OPennException("Cannot find TEI file: %s", (self._tei_file,))

        # Validate the TEI?
        #   - Has values: title
        #   -
        #   -
        openn_tei = self._openn_tei()

        errors = []
        if openn_tei.title is None:
            errors.append("Title cannot be blank")
        if openn_tei.licences is None or len(openn_tei.licences) == 0:
            errors.append("At least one licence must be provided")
        if len(errors) > 0:
            msg = "TEI validation errors found: %s"
            raise OPennException(msg % (' ;'.join(errors),))
