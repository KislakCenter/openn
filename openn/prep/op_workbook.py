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
from openn.prep.validatable_sheet import ValidatableSheet
from openn.prep.workbook_data import WorkbookData

from openpyxl import load_workbook
from openpyxl.workbook import workbook

import warnings


class OPWorkbook:

    ######################################################################
    # Instance methods
    ######################################################################

    def __init__(self, xlsx_file, config):
        """Create a new OPWorkbook and find all description sheet headings.

        """
        self.config      = config['sheet_config']
        self.xlsx_path   = xlsx_file
        warnings.simplefilter("ignore")
        self.workbook    = load_workbook(self.xlsx_path)
        warnings.simplefilter("always")
        self.errors      = []
        self.warnings    = []
        self._sheets      = {}
        self._set_sheets()

    # --------------------------------------------------------------------
    # Validation
    # --------------------------------------------------------------------

    def get_sheet(self,attr):
        return self._sheets.get(attr, None)

    @property
    def description(self):
        return self.get_sheet('description')

    @property
    def pages(self):
        return self.get_sheet('pages')

    def data(self):
        """Return a dict containing SheetData objects for all configured
        sheets.  Dict keys are sheet attr names ('pages',
        'description').

        """
        data = WorkbookData()
        for sheet in self.sheets():
            data.add_sheet_data(sheet.sheet_data())

        return data

    def validate_pages(self):
        self.pages.validate()

    def validate_description(self):
        self.description.validate()

    def has_description_errors(self):
        return len(self.description.errors) > 0

    def has_description_warnings(self):
        return self.description.has_errors()

    def has_page_errors(self):
        return self.pages.has_errors()

    def sheets(self):
        for attr in self._sheets:
            yield self._sheets[attr]

    def file_errors(self, ):
        errors = []
        for sheet in self.sheets():
            errors.extend(sheet.file_errors)
        return errors

    def metadata_errors(self):
        errors = []
        for sheet in self.sheets():
            errors.extend(sheet.errors)
        return errors

    def has_file_errors(self):
        for sheet in self.sheets():
            if sheet.has_file_errors(): return True
        return False

    def has_metadata_errors(self):
        for sheet in self.sheets():
            if sheet.has_errors(): return True
        return False

    def validate_file_lists(self):
        for sheet in self.sheets():
            sheet.validate_file_lists()

            if self.has_file_errors():
                msg = [ "Errors found checking files in workbook: %s" % (
                    self.xlsx_path,) ] + self.file_errors()
                raise OPennException('\n'.join(msg))

    def validate(self):
        for sheet in self.sheets():
            sheet.validate()
            if self.has_metadata_errors():
                msg = [ "Errors found in metadata for workbook: %s" % (
                    self.xlsx_path,) ] + self.metadata_errors()
                raise OPennException('\n'.join(msg))

    # --------------------------------------------------------------------
    # Properties
    # --------------------------------------------------------------------

    @property
    def workbook_dir(self):
        return os.path.dirname(self.xlsx_path)

    # --------------------------------------------------------------------
    # _ methods
    # --------------------------------------------------------------------
    def _set_sheets(self):

        for attr in self.config:
            sheet_name = self.config[attr]['sheet_name']
            worksheet = self.workbook[sheet_name]
            vsheet = ValidatableSheet(
                worksheet, self.xlsx_path, deepcopy(self.config[attr]))
            self._sheets[attr] = vsheet
