#!/usr/bin/env python
# -*- coding: utf-8 -*-

from openn.prep.validatable_sheet import ValidatableSheet

class DescriptionSheet(ValidatableSheet):

    ######################################################################
    # Instance methods
    ######################################################################

    def __init__(self, op_workbook, config={}):
        super(DescriptionSheet, self).__init__(op_workbook, config)
