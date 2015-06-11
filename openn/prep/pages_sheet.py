#!/usr/bin/env python
# -*- coding: utf-8 -*-

from openn.prep.validatable_sheet import ValidatableSheet

class PagesSheet(ValidatableSheet):

    ######################################################################
    # Instance methods
    ######################################################################

    def __init__(self, worksheet, workbook_path, config={}):
        super(PagesSheet, self).__init__(worksheet, workbook_path, config)
