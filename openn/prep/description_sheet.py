#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import re

from copy import deepcopy

from openn.prep import langs
from openn.openn_exception import OPennException
from openn.prep.validatable_sheet import ValidatableSheet

class DescriptionSheet(ValidatableSheet):

    ######################################################################
    # Instance methods
    ######################################################################

    def __init__(self, op_workbook, config={}):
        super(DescriptionSheet, self).__init__(op_workbook, config)

    # --------------------------------------------------------------------
    # Validation
    # --------------------------------------------------------------------

    def validate(self):
        self.check_required_headings()
        self.check_description_values()

    def check_required_headings(self):
        for field in self.required_fields:
            if not field['locus']:
                msg = 'Required field is missing: %s' % (field['field_name'],)
                self.errors.append(msg)

    def check_description_values(self):
        for attr in self.fields:
            self.validate_field(attr)
