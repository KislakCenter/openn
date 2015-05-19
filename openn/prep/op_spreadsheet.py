#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import simplejson
import re

from openn.prep import langs

from openpyxl import load_workbook
from openpyxl.workbook import Workbook


class OPSpreadsheet:

    MIN_YEAR = -5000
    MAX_YEAR = 3000

    # conversion of John Gruber's URI RE adapted from:
    #   https://gist.github.com/uogbuji/705383
    URI_RE = re.compile(ur'(?i)\b((?:[a-z][\w-]+:(?:/{1,3}|[a-z0-9%])|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:\'".,<>?\xab\xbb\u201c\u201d\u2018\u2019]))')

    YEAR_RE = re.compile(ur'^-?\d{1,4}$')
    # this an imperfect regex for this purpose and can only be assumed
    # to match most email address
    # It's taken from here:
    #
    #   http://www.regular-expressions.info/email.html
    #
    # For the ugly details on regexes and email address, see this discussion:
    #
    #   http://stackoverflow.com/questions/201323/using-a-regular-expression-to-validate-an-email-address
    #
    EMAIL_RE = re.compile(r'\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,4}\b', re.I)

    # The offset to use to find the first value column; the data
    # starts 2 columns past the column the headering is in:
    #
    # Field          | Req't | Entry 1
    # ---------------|-------|--------
    # Call number    |   R   | MS ABC 123
    #
    FIELD_COLUMN_OFFSET = 2

    def __init__(self, xlsx_file, config):
        self.config              = config
        self.xlsx_path           = xlsx_file
        self.workbook            = load_workbook(self.xlsx_path)
        self.validation_errors   = []
        self.validation_warnings = []
        self.set_headings()
        # self.set_column_offset()

    def has_description_errors(self):
        return len(self.validation_errors) > 0

    def has_description_warnings(self):
        return len(self.validation_warnings) > 0

    def validate_description(self):
        self.check_required_headings()
        self.check_description_values()

    def check_required_headings(self):
        for field in self.required_fields:
            if not field['locus']:
                msg = 'Required field is missing: %s' % (field['field_name'],)
                self.validation_errors.append(msg)

    def check_description_values(self):
        for attr in self.fields:
            self.validate_field(attr)

    def extract_values(self, heading_locus):
        vals = []
        row = heading_locus['row']
        # read the first 20 columns past the heading locus
        data_col = heading_locus['col'] + self.FIELD_COLUMN_OFFSET
        for col in xrange(data_col, data_col + 21):
            cell = self.description_sheet.cell(column=col,row=row)
            if cell is not None and cell.value != '':
                vals.append(cell.value)
            else:
                vals.append(None)

        # strip off trailing Nones
        while len(vals) > 0 and vals[-1] is None:
            del vals[-1]

        return vals

    @staticmethod
    def is_valid_uri(val):
        return OPSpreadsheet.URI_RE.match(val) is not None

    @staticmethod
    def is_valid_year(val):
        return OPSpreadsheet.YEAR_RE.match(str(val)) and \
            int(val) in xrange(OPSpreadsheet.MIN_YEAR, OPSpreadsheet.MAX_YEAR + 1)

    @staticmethod
    def is_valid_email(val):
        return OPSpreadsheet.EMAIL_RE.match(val) is not None

    @staticmethod
    def is_valid_lang(val):
        return langs.is_valid_lang(val)

    def validate_field(self, attr):
        # first see if the field is missing and required
        details = self.fields[attr]
        field_name = details['field_name']
        if details['locus']:
            # the field is present; keep going
            pass
        elif details['required']:
            # not present, but required; add an error and return
            msg = 'Required field is missing: %s' % (field_name,)
            self.validation_errors.append(msg)
            return
        else:
            # not present and not required; add no errors and return
            return

        values = self.extract_values(details['locus'])
        if details['required'] and len(values) == 0:
            # required field is blank; add error and return
            msg = '%s cannot be blank' % (field_name,)
            self.validation_errors.append(msg)
            return

        # check repeating
        if details['repeating'] == False and len(values) > 1:
            extras = [x for x in values[1:] if x is not None]
            for v in values[1:]:
                if v is not None:
                    msg = "Extra value found in non-repeating field %s: %s" % (field_name, v)
                    self.validation_errors.append(msg)

        for val in values:
            self.validate_data_type(val, details)

    def format_error(self, field_name, value, data_type):
        return "%s is not a valid %s: %s" % (field_name, data_type, value)

    def validate_data_type(self, value, details):
        data_type  = details['data_type']
        field_name = details['data_type']

        if data_type == 'year' and not OPSpreadsheet.is_valid_year(value):
            self.validation_errors.append(
                self.format_error(field_name, value, data_type))
        elif data_type == 'uri' and not OPSpreadsheet.is_valid_uri(value):
            self.validation_errors.append(
                self.format_error(field_name, value, data_type))
        elif data_type == 'lang' and not OPSpreadsheet.is_valid_lang(value):
            self.validation_errors.append(
                self.format_error(field_name, value, data_type))
        elif data_type == 'email' and not OPSpreadsheet.is_valid_email(value):
            self.validation_warnings.append(
                self.format_error(field_name, value, data_type))

    @property
    def description_sheet(self):
	return self.workbook.get_sheet_by_name('Description')

    @property
    def required_fields(self):
        return [ x for x in self.fields.itervalues() if x['required'] ]

    @property
    def fields(self):
        return self.config['fields']

    # @property
    # def field_column_offset(self):
    #     return self._field_column_offset

    def find_heading_locus(self, field_name):
        locus = []
        sheet = self.description_sheet
        for row in xrange(1, sheet.max_row):
            # look at this crap: min_col, but max_column
            for col in xrange(1, 20):
                cell = self.description_sheet.cell(column=col, row=row)
                value = cell.value if cell is not None else ''
                if self.normalize(value) == self.normalize(field_name):
                    return {'col': col,'row': row }

    def set_headings(self):
        for attr in self.fields:
            details          = self.fields[attr]
            field_name       = details['field_name']
            locus            = self.find_heading_locus(field_name)
            details['locus'] = locus

    # def set_column_offset(self):
    #     locus = self.find_heading_locus('Entry 1')
    #     if locus is None:
    #         raise OPennException("Cannot find column heading for Entry 1")
    #     col = locus['col']
    #     self._field_column_offset = col - 1
    #     print "_field_column_offset=%d" % self._field_column_offset

    def normalize(self, s):
        if s is not None:
            return re.sub(r'\W+', '', str(s)).lower()
