#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import re

from copy import deepcopy

from openn.prep import langs
from openn.openn_exception import OPennException
from openn.prep.description_sheet import DescriptionSheet
from openn.prep.pages_sheet import PagesSheet

from openpyxl import load_workbook
from openpyxl.workbook import workbook


class OPWorkbook:

    ######################################################################
    # Instance methods
    ######################################################################

    def __init__(self, xlsx_file, config):
        """Create a new OPWorkbook and find all description sheet headings.

        """
        self.config      = deepcopy(config)
        self.xlsx_path   = xlsx_file
        self.workbook    = load_workbook(self.xlsx_path)
        self.errors      = []
        self.warnings    = []
        self.description = DescriptionSheet(self,self.config['description'])
        self.pages       = PagesSheet(self,self.config['pages'])

    # --------------------------------------------------------------------
    # Validation
    # --------------------------------------------------------------------

    def has_description_errors(self):
        return len(self.description.errors) > 0

    def has_description_warnings(self):
        return self.description.has_errors()

    def has_page_errors(self):
        return self.pages.has_errors()

    def has_file_errors(self):
        return self.pages.has_file_errors()

    def has_metadata_errors(self):
        return self.has_page_errors() or self.has_description_errors()

    def validate_description(self):
        self.description.validate()

    def validate_pages(self):
        self.pages.validate()

    def validate_file_lists(self):
        self.pages.validate_file_lists()
        if self.has_file_errors():
            msg = [ "Errors found checking files in workbook: %s" % (self.xlsx_path,) ] + \
                  self.pages.file_errors
            raise OPennException('\n'.join(msg))

    def validate(self):
        self.validate_description()
        self.validate_pages()
        if self.has_metadata_errors():
            msg = [ "Errors found in metadata for workbook: %s" % (self.xlsx_path,) ] + \
                  self.pages.errors + self.description.errors
            raise OPennException('\n'.join(msg))

    def get_sheet(self, sheet_name):
        return self.workbook.get_sheet_by_name(sheet_name)

    # --------------------------------------------------------------------
    # Properties
    # --------------------------------------------------------------------

    @property
    def workbook_dir(self):
        return os.path.dirname(self.xlsx_path)
