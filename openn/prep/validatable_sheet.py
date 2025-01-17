#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
# import re
import itertools
import logging
import regex
from copy import deepcopy

from openn.prep import langs
from openn.openn_exception import OPennException
from openn.prep.sheet_data import SheetData
from openn.openn_functions import *

class ValidatableSheet(object):

    logger = logging.getLogger(__name__)

    MIN_YEAR = -5000
    MAX_YEAR = 3000

    HEADER_COLUMN_MAX = 300
    HEADER_ROW_MAX = 300

    # No-break space
    NO_BREAK_SPACE = '\u00A0'
    # Match non-breaking space followed or proceeded by one or zero
    # spaces
    NO_BREAK_SPACE_RE = regex.compile(" ?%s ?" % (NO_BREAK_SPACE,), regex.UNICODE)
    # For stray right-to-left and left-to-right characters
    RTL = '\u200F'.decode( 'unicode-escape' )
    LTR = '\u200E'.decode( 'unicode-escape' )
    BIDI_RE = regex.compile("[%s%s]+" % (RTL, LTR), regex.UNICODE)
    # Fixing MS `smart` quotes
    # ‘ (U+2018) LEFT SINGLE QUOTATION MARK
    LEFT_SINGLE_QUOTATION_MARK = '\u2018'.decode('unicode-escape')
    # ’ (U+2019) RIGHT SINGLE QUOTATION MARK
    RIGHT_SINGLE_QUOTATION_MARK  = '\u2019'.decode('unicode-escape')
    SINGLE_QUOTE_RE = regex.compile("[%s%s]" % (
        RIGHT_SINGLE_QUOTATION_MARK, LEFT_SINGLE_QUOTATION_MARK), regex.UNICODE)

    # “ (U+201C) LEFT DOUBLE QUOTATION MARK
    LEFT_DOUBLE_QUOTATION_MARK = '\u201C'.decode('unicode-escape')
    # ” (U+201D) RIGHT DOUBLE QUOTATION MARK
    RIGHT_DOUBLE_QUOTATION_MARK = '\u201D'.decode('unicode-escape')
    DOUBLE_QUOTE_RE = regex.compile("[%s%s]" % (
        RIGHT_DOUBLE_QUOTATION_MARK, LEFT_DOUBLE_QUOTATION_MARK), regex.UNICODE)

    # conversion of John Gruber's URI RE adapted from:
    #   https://gist.github.com/uogbuji/705383
    URI_RE = regex.compile(ur'(?i)\b((?:[a-z][\w-]+:(?:/{1,3}|[a-z0-9%])|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:\'".,<>?\xab\xbb\u201c\u201d\u2018\u2019]))')

    YEAR_RE = regex.compile(ur'^-?\d{4}$')

    WORD_RE = regex.compile(ur'^(\p{L}|\p{N}|\p{P}|\p{S})+$')
    INTEGER_RE = regex.compile(ur'^\d+$')
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
    EMAIL_RE = regex.compile(r'\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,4}\b', regex.I)

    # openpyxl numbers colunms starting at 1; put None at 0 index;
    # this is the first 520 columns.  Wish Python had Ruby's
    # String#succ! method.
    COLUMNS = ( None,
                'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
                'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
                'AA', 'AB', 'AC', 'AD', 'AE', 'AF', 'AG', 'AH', 'AI', 'AJ', 'AK',
                'AL', 'AM', 'AN', 'AO', 'AP', 'AQ', 'AR', 'AS', 'AT', 'AU', 'AV',
                'AW', 'AX', 'AY', 'AZ', 'BA', 'BB', 'BC', 'BD', 'BE', 'BF', 'BG',
                'BH', 'BI', 'BJ', 'BK', 'BL', 'BM', 'BN', 'BO', 'BP', 'BQ', 'BR',
                'BS', 'BT', 'BU', 'BV', 'BW', 'BX', 'BY', 'BZ', 'CA', 'CB', 'CC',
                'CD', 'CE', 'CF', 'CG', 'CH', 'CI', 'CJ', 'CK', 'CL', 'CM', 'CN',
                'CO', 'CP', 'CQ', 'CR', 'CS', 'CT', 'CU', 'CV', 'CW', 'CX', 'CY',
                'CZ', 'DA', 'DB', 'DC', 'DD', 'DE', 'DF', 'DG', 'DH', 'DI', 'DJ',
                'DK', 'DL', 'DM', 'DN', 'DO', 'DP', 'DQ', 'DR', 'DS', 'DT', 'DU',
                'DV', 'DW', 'DX', 'DY', 'DZ', 'EA', 'EB', 'EC', 'ED', 'EE', 'EF',
                'EG', 'EH', 'EI', 'EJ', 'EK', 'EL', 'EM', 'EN', 'EO', 'EP', 'EQ',
                'ER', 'ES', 'ET', 'EU', 'EV', 'EW', 'EX', 'EY', 'EZ', 'FA', 'FB',
                'FC', 'FD', 'FE', 'FF', 'FG', 'FH', 'FI', 'FJ', 'FK', 'FL', 'FM',
                'FN', 'FO', 'FP', 'FQ', 'FR', 'FS', 'FT', 'FU', 'FV', 'FW', 'FX',
                'FY', 'FZ', 'GA', 'GB', 'GC', 'GD', 'GE', 'GF', 'GG', 'GH', 'GI',
                'GJ', 'GK', 'GL', 'GM', 'GN', 'GO', 'GP', 'GQ', 'GR', 'GS', 'GT',
                'GU', 'GV', 'GW', 'GX', 'GY', 'GZ', 'HA', 'HB', 'HC', 'HD', 'HE',
                'HF', 'HG', 'HH', 'HI', 'HJ', 'HK', 'HL', 'HM', 'HN', 'HO', 'HP',
                'HQ', 'HR', 'HS', 'HT', 'HU', 'HV', 'HW', 'HX', 'HY', 'HZ', 'IA',
                'IB', 'IC', 'ID', 'IE', 'IF', 'IG', 'IH', 'II', 'IJ', 'IK', 'IL',
                'IM', 'IN', 'IO', 'IP', 'IQ', 'IR', 'IS', 'IT', 'IU', 'IV', 'IW',
                'IX', 'IY', 'IZ', 'JA', 'JB', 'JC', 'JD', 'JE', 'JF', 'JG', 'JH',
                'JI', 'JJ', 'JK', 'JL', 'JM', 'JN', 'JO', 'JP', 'JQ', 'JR', 'JS',
                'JT', 'JU', 'JV', 'JW', 'JX', 'JY', 'JZ', 'KA', 'KB', 'KC', 'KD',
                'KE', 'KF', 'KG', 'KH', 'KI', 'KJ', 'KK', 'KL', 'KM', 'KN', 'KO',
                'KP', 'KQ', 'KR', 'KS', 'KT', 'KU', 'KV', 'KW', 'KX', 'KY', 'KZ',
                'LA', 'LB', 'LC', 'LD', 'LE', 'LF', 'LG', 'LH', 'LI', 'LJ', 'LK',
                'LL', 'LM', 'LN', 'LO', 'LP', 'LQ', 'LR', 'LS', 'LT', 'LU', 'LV',
                'LW', 'LX', 'LY', 'LZ', 'MA', 'MB', 'MC', 'MD', 'ME', 'MF', 'MG',
                'MH', 'MI', 'MJ', 'MK', 'ML', 'MM', 'MN', 'MO', 'MP', 'MQ', 'MR',
                'MS', 'MT', 'MU', 'MV', 'MW', 'MX', 'MY', 'MZ', 'NA', 'NB', 'NC',
                'ND', 'NE', 'NF', 'NG', 'NH', 'NI', 'NJ', 'NK', 'NL', 'NM', 'NN',
                'NO', 'NP', 'NQ', 'NR', 'NS', 'NT', 'NU', 'NV', 'NW', 'NX', 'NY',
                'NZ', 'OA', 'OB', 'OC', 'OD', 'OE', 'OF', 'OG', 'OH', 'OI', 'OJ',
                'OK', 'OL', 'OM', 'ON', 'OO', 'OP', 'OQ', 'OR', 'OS', 'OT', 'OU',
                'OV', 'OW', 'OX', 'OY', 'OZ', 'PA', 'PB', 'PC', 'PD', 'PE', 'PF',
                'PG', 'PH', 'PI', 'PJ', 'PK', 'PL', 'PM', 'PN', 'PO', 'PP', 'PQ',
                'PR', 'PS', 'PT', 'PU', 'PV', 'PW', 'PX', 'PY', 'PZ', 'QA', 'QB',
                'QC', 'QD', 'QE', 'QF', 'QG', 'QH', 'QI', 'QJ', 'QK', 'QL', 'QM',
                'QN', 'QO', 'QP', 'QQ', 'QR', 'QS', 'QT', 'QU', 'QV', 'QW', 'QX',
                'QY', 'QZ', 'RA', 'RB', 'RC', 'RD', 'RE', 'RF', 'RG', 'RH', 'RI',
                'RJ', 'RK', 'RL', 'RM', 'RN', 'RO', 'RP', 'RQ', 'RR', 'RS', 'RT',
                'RU', 'RV', 'RW', 'RX', 'RY', 'RZ', 'SA', 'SB', 'SC', 'SD', 'SE',
                'SF', 'SG', 'SH', 'SI', 'SJ', 'SK', 'SL', 'SM', 'SN', 'SO', 'SP',
                'SQ', 'SR', 'SS', 'ST', 'SU', 'SV', 'SW', 'SX', 'SY', 'SZ' )

    ######################################################################
    # Static methods
    ######################################################################

    @staticmethod
    def is_valid_uri(val):
        return ValidatableSheet.URI_RE.match(val) is not None

    @staticmethod
    def is_valid_year(val):
        return ValidatableSheet.YEAR_RE.match(unicode(val).strip()) and \
            int(val) in xrange(ValidatableSheet.MIN_YEAR, ValidatableSheet.MAX_YEAR + 1)

    @staticmethod
    def is_valid_word(val):
        return ValidatableSheet.WORD_RE.match(unicode(val).strip())

    @staticmethod
    def is_empty_value(value):
        return value is None or len(unicode(value).strip()) == 0

    @staticmethod
    def is_nonempty_value(value):
        return not ValidatableSheet.is_empty_value(value)

    @staticmethod
    def is_valid_integer(val):
        # Don't parse empty values
        if ValidatableSheet.is_empty_value(val): return True

        try:
            return (int(val) + 0 == int(val)) and \
                ValidatableSheet.INTEGER_RE.match(unicode(val).strip())
        except (TypeError, ValueError):
            return False

    @staticmethod
    def is_valid_email(val):
        return ValidatableSheet.EMAIL_RE.match(val) is not None

    @staticmethod
    def is_valid_lang(val):
        return langs.is_valid_lang(val)

    @staticmethod
    def is_value_in_list(value, val_list, case_senstive=False):
        if case_senstive:
            return value in val_list
        else:
            return unicode(value).lower() in [ unicode(x).lower() for x in val_list ]

    @staticmethod
    def column_letter(colindex):
        if colindex < len(ValidatableSheet.COLUMNS):
            return ValidatableSheet.COLUMNS[colindex]
        else:
            return "%d-" % (colindex,)

    @staticmethod
    def cell_address(col, row):
        return ''.join([ ValidatableSheet.column_letter(col), unicode(row) ])

    @staticmethod
    def normalize(s):
        if s is not None:
            u = ValidatableSheet.fix_unicode(s)
            return regex.sub(r'\W+', '', u).lower()

    @staticmethod
    def fix_unicode(val):
        u = ValidatableSheet.BIDI_RE.sub(u'', unicode(val).strip())
        u = ValidatableSheet.SINGLE_QUOTE_RE.sub(u"'", u)
        u = ValidatableSheet.DOUBLE_QUOTE_RE.sub(u'"', u)
        u = ValidatableSheet.NO_BREAK_SPACE_RE.sub(u' ', u)
        return u


    ######################################################################
    # Instance methods
    ######################################################################

    def __init__(self, worksheet, xlsx_path, config={}):
        self.xlsx_path = xlsx_path
        self.worksheet     = worksheet
        self.config        = deepcopy(config)
        self.file_errors   = []
        self.errors        = []
        self.warnings      = []
        self._heading_column = None
        self._heading_row = None
        self.__repeat_limit = None
        self._set_headings()

    # --------------------------------------------------------------------
    # Properties
    # --------------------------------------------------------------------

    @property
    def required_fields(self):
        """Return details dict for all fields where 'required' is True.

        """
        return [ x for x in self.fields.itervalues() if x['required'] ]

    @property
    def workbook_dir(self):
        return os.path.dirname(self.xlsx_path)

    @property
    def file_lists(self):
        return [ x for x in self.fields if self.is_file_list(x) ]

    @property
    def fields(self):
        return self.config['fields']

    @property
    def sheet(self):
        return self.worksheet

    @property
    def sheet_name(self):
        return self.config['sheet_name']

    @property
    def data_offset(self):
        """The offset from the heading row or column to find first value.  The
        offset must be in the sheet's configuration as 'data_offset':

            'description': {
                'sheet_name': 'Description',
                'heading_type': 'row',
                'data_offset': 2,
                'fields': {
                    'field_1': {
                        'field_name': 'Field 1',
                        'required': False,
                        'repeating': True,
                        'data_type': 'string'
                    },
             ...


        In the example below, with row headings, the field names
        'Repository' and 'Call number' are in column 1 and the data in
        column 3 ('Penn Libraries' and 'MS ABC 123').  Therefore, the
        offset is 2.

        ---------------|-------|-----------------
        Repository     |   R   | Penn Libraries
        ---------------|-------|-----------------
        Call number    |   R   | MS ABC 123
        ---------------|-------|-----------------
        ...            |       |
        ---------------|-------|-----------------

        """
        return self.config.get('data_offset', 1)

    @property
    def heading_type(self):
        """The heading type is either 'row' or 'column'.  By default, 'column'
        is used.  The meaning is straightforward.  If headings label
        rows, the sheet's 'heading_type' is 'row'; if they label
        columns then the value is 'column'.


            'description': {
                'sheet_name': 'Description',
                'heading_type': 'row',
                'data_offset': 2,
                'fields': {
                    'field_1': {
                        'field_name': 'Field 1',
                        'required': False,
                        'repeating': True,
                        'data_type': 'string'
                    },
             ...


        """
        return self.config.get('heading_type', 'column').lower()

    @property
    def repeat_limit(self):

        """

        Max repeat `repeat_limit` is an optional parameter that helps the
        worksheet calculate a maximum number of rows or columns to check when
        inspecting a field. If `None`, the spreadsheet `max_column` or
        `max_row` value is used.

        If "fixed", an integer should be provided:

                    "sheet_config": {
                        "description": {
                            "sheet_name": "Description",
                            "data_offset": 2,
                            "heading_type": "row",
                            "repeat_limit": {
                                "fixed": 50
                            },
                            "fields": { ...

        In the above case, exraction will not check more than 50 columns.

        If "fields", a list of fields should be provided.

                "pages": {
                    "sheet_name": "Pages",
                    "data_offset": 1,
                    "heading_type": "column",
                    "repeat_limit": {
                        "fields": [ "file_name", "display_page" ]
                    },
                    "fields": { ....

        In the above case, the `repeat_limit` number will be the maximum of the
        last non-blank row for `file_name` and `display_page`.

        """

        return self.config.get('repeat_limit', None)

    @property
    def max_column(self):
        """
        Return the maximum as configured for the spreadsheet or the
        spreadsheet's actual last column whichver is lower.

        Example:

                "pages": {
                    "sheet_name": "Pages",
                    "data_offset": 1,
                    "heading_type": "column",
                    "repeat_limit": {
                        "fields": [ "file_name", "display_page" ]
                    },
                    "max_column": 200,
                    "max_row": 10000,
                    ...

        The max_column configuration value is not intended to limit the number
        of items that may be in a spreadsheet, but to prevent a situation
        which can happen with some spreadsheets where the last row or column
        goes to the spreadsheet's limit; e.g., row 1,048,576 or column 16,384,
        thus bogging down computation. Therefore, the max_column value should
        be well more than any possible number of values, while being below the
        spreadsheet limit.

        """

        vals = [self.sheet.max_column]

        if self.config.get('max_column', None) is not None:
            vals.append(self.config.get('max_column'))

        return min(vals)

    @property
    def max_row(self):
        """
        Return the maximum as configured for the spreadsheet or the
        spreadsheet's actual last row whichver is lower.

         Example:

                "pages": {
                    "sheet_name": "Pages",
                    "data_offset": 1,
                    "heading_type": "column",
                    "repeat_limit": {
                        "fields": [ "file_name", "display_page" ]
                    },
                    "max_column": 200,
                    "max_row": 10000,
                    ...

        The max_row configuration value is not intended to limit the number of
        items that may be in a spreadsheet, but to prevent a situation which
        can happen with some spreadsheets where the last row or column goes to
        the spreadsheet's limit; e.g., row 1,048,576 or column 16,384, thus
        bogging down computation. Therefore, the max_row value should be well
        more than any possible number of values, while being below the
        spreadsheet limit.

        """
        vals = [self.sheet.max_row]

        if self.config.get('max_row', None) is not None:
            vals.append(self.config.get('max_row'))

        return min(vals)

    # --------------------------------------------------------------------
    # Validation
    # --------------------------------------------------------------------

    def has_errors(self, ):
        return self.errors is not None and len(self.errors) > 0

    def has_file_errors(self):
        return self.file_errors is not None and len(self.file_errors) > 0

    def add_error(self, attr, index, msg):
        self._add_error(attr=attr, index=index, msg=msg,
                        error_list=self.errors)

    def add_file_error(self, attr, index, msg):
        self._add_error(attr=attr, index=index, msg=msg,
                        error_list=self.file_errors)

    def validate(self):
        self.check_required_headings()
        self.check_field_values()

    def check_field_values(self):
        for attr in self.fields:
            self.validate_field(attr)

    def check_required_headings(self):
        for field in self.required_fields:
            if not field['locus']:
                msg = 'Required field is missing: %s' % (field['field_name'],)
                self.errors.append(msg)

    def validate_file_lists(self):
        for attr in self.file_lists:
            if not self.locus(attr):
                pass
            else:
                wdir = self.workbook_dir
                allow_blank=self.is_optional(attr)
                self.validate_file_list(attr, wdir, allow_blank)

    def validate_file_list(self, attr, directory, allow_blank=True):
        values = self.values(attr)
        for i in xrange(len(values)):
            fname  = values[i]
            if self.is_empty_value(fname):
                if not allow_blank:
                    msg = '%s: File list cannot have empty values' % (self.field_name(attr),)
                    self.add_file_error(attr, i, msg)
            else:
                path = os.path.join(directory, str(fname))
                if not os.path.exists(path):
                    msg = '%s: Could not find expected file: %s' % (self.field_name(attr), path)
                    self.add_file_error(attr, i, msg)

    def validate_blank_if_other_nonempty(self, attr, other_attr):
        if self.is_empty(other_attr): return

        values, others = self.paired_values(attr, other_attr)
        for i in xrange(len(values)):
            if (self.is_nonempty_value(values[i]) and
                self.is_nonempty_value(others[i])):
                msg = "'%s' must be empty if '%s' has a value; found: '%s'" % (
                    self.field_name(attr), self.field_name(other_attr),
                    values[i])
                self.add_error(attr, i, msg)

    def validate_blank_if_other_empty(self, attr, other_attr):
        if self.is_empty(attr): return

        values, others = self.paired_values(attr, other_attr)
        for i in xrange(len(values)):
            if (self.is_nonempty_value(values[i]) and
                self.is_empty_value(others[i])):
                msg = "'%s' must be empty if '%s' is empty; found: '%s'" % (
                    self.field_name(attr), self.field_name(other_attr),
                    values[i])
                self.add_error(attr, i, msg)

    def validate_blank_if_other_in_list(self, attr, other_attr, val_list):
        if self.is_empty(attr): return

        values, others = self.paired_values(attr, other_attr)
        for i in xrange(len(values)):
            if (self.is_nonempty_value(values[i]) and
                others[i] is not None and
                self.is_value_in_list(others[i], val_list)):
                msg = "'%s' must be empty if '%s' is '%s'; found: '%s'" % (
                    self.field_name(attr), self.field_name(other_attr),
                    others[i], values[i])
                self.add_error(attr, i, msg)

    def validate_blank(self, attr):
        """If 'attr' has a blank rule and field is non-empty, validate
        whether field may have a value.

        """
        if self.blank_rule(attr) is None or self.is_empty(attr): return

        blankrule    = self.fields[attr]['blank']
        ifclause     = blankrule['if']
        other_attr   = ifclause['field']
        condition    = ifclause['is']

        if condition == 'EMPTY':
            self.validate_blank_if_other_empty(attr, other_attr)
        elif condition == 'NONEMPTY':
            self.validate_blank_if_other_nonempty(attr, other_attr)
        elif isinstance(condition,list):
            self.validate_blank_if_other_in_list(attr, other_attr, condition)
        else:
            raise OPennException("Unknown condition type: '%s'" % (condition,))

    def validate_required_if_other_empty(self, attr, other_attr):
        field_name = self.field_name(attr)
        other_name = self.field_name(other_attr)
        if self.is_empty(attr) and self.is_empty(other_attr):
            msg = "'%s' cannot be empty if '%s' is empty" % (
                field_name, other_name)
            self.add_error(attr, 0, msg)
        elif self.is_empty(other_attr):
            values, others = self.paired_values(attr, other_attr)

            for i in xrange(len(values)):
                if (self.is_empty_value(values[i]) and (
                        len(others) <= i or self.is_empty_value(others[i]))):
                    msg = "'%s' cannot be empty if '%s' is empty" % (
                        field_name, other_name)
                    self.add_error(attr, i, msg)

    def validate_required_if_other_nonempty(self, attr, other_attr):
        if self.is_empty(other_attr): return

        values, others = self.paired_values(attr, other_attr)
        for i in xrange(len(values)):
            if (self.is_empty_value(values[i]) and
                self.is_nonempty_value(others[i])):
                field_name = self.field_name(attr)
                other_name = self.field_name(other_attr)
                msg = "'%s' cannot be empty if '%s' has a value" % (
                    field_name, other_name)
                self.add_error(attr, i, msg)

    def validate_required_if_other_in_list(self, attr, other_attr, val_list):
        if self.is_empty(other_attr): return

        values, others = self.paired_values(attr, other_attr)
        for i in xrange(len(values)):
            if (self.is_empty_value(values[i]) and
                others[i] is not None and
                self.is_value_in_list(others[i], val_list)):
                msg = "'%s' cannot be empty if '%s' is '%s'" % (
                    self.field_name(attr), self.field_name(other_attr), others[i])
                self.add_error(attr, i, msg)

    def validate_conditional(self, attr, required):
        """Validate a conditional requirement rule."""
        ifclause     = required['if']
        other_attr   = ifclause['field']
        condition    = ifclause['is']

        if condition == 'EMPTY':
            self.validate_required_if_other_empty(attr,other_attr)
        elif condition == 'NONEMPTY':
            self.validate_required_if_other_nonempty(attr, other_attr)
        elif isinstance(condition, list):
            self.validate_required_if_other_in_list(attr, other_attr, condition)
        else:
            raise OPennException('Unknown condition type: %s' % (condition,))

    def validate_requirement(self, attr):
        """Validate required or conditionally required field if 'required' is
        present and non-False.

        """
        details = self.fields[attr]
        field_name = details['field_name']
        required = details['required']
        if required == True and self.is_empty(attr):
            msg = '%s cannot be empty' % (details['field_name'],)
            self.add_error(attr, 0, msg)
        elif isinstance(required, dict):
            self.validate_conditional(attr, required)

    def validate_value_list(self, attr):
        """Validate field whose values must come from a list if 'value_list'
        present.

        """
        value_list = self.value_list(attr)
        if value_list is None: return

        for val in self.values(attr):
            if val is None or self.is_value_in_list(val, value_list):
                pass
            else:
                msg = "'%s' value '%s' not valid; expected one of: %s" % (
                    self.field_name(attr), val, ', '.join(self._list_quoted(value_list)))
                self.add_error(attr, 0, msg)

    def validate_repeating(self, attr):
        """Validate non-repeating fields if 'repeating' set to False.

        """
        if not self.repeating(attr) and len(self.values(attr)) > 1:
            msg = 'More than one value found in non-repeating field %s: %s' % (
                self.field_name(attr), ', '.join(self._values_quoted(attr)))
            self.add_error(attr, 0, msg)

    def validate_field(self, attr):
        """Perform all validations for field."""
        # first see if the field is missing
        if self.is_field_missing(attr): return
        try:
            self.validate_requirement(attr)
            self.validate_uniqueness(attr)
            self.validate_blank(attr)
            self.validate_value_list(attr)
            self.validate_repeating(attr)
            self.validate_data_type(attr)
        except Exception as ex:
            self.logger.error("Error checking attribute: %s", attr)
            raise

    def validate_data_type(self, attr):
        """Validate all values for field against configured 'data_type'.

        """
        data_type = self.data_type(attr)
        field_name = self.field_name(attr)
        for val in self.values(attr):
            # don't try to validate data type if None
            if val is not None:
                self._do_type_validation(field_name, val, self.data_type(attr))

    def validate_uniqueness(self, attr):
        # don't validate non-existent field
        if self.fields.get(attr, None) is None: return
        # don't validate if no uniqueness constraint
        if not self.fields[attr].get('unique', False): return

        values = self._extract_values(attr)
        unique_values = set(values)
        # don't validate if all values unique
        if len(values) == len(unique_values): return

        dups = self._get_dups(values)
        specs = [ "%s (%dx)" % (x[0], x[1]) for x in dups ]
        msg = "'%s' cannot have duplicate values; found: %s" % (
            self.field_name(attr), '; '.join(specs))
        self.add_error(attr, 0, msg)

    # --------------------------------------------------------------------
    # Field accessors
    # --------------------------------------------------------------------
    def sheet_data(self):
        """
        Return all the data values from this sheet.
        """
        return SheetData(self.sheet_name, self.data_dict())

    def data_dict(self):
        data = {}
        for attr in self.fields:
            data[attr] = deepcopy(self.values(attr))

        return data

    def composite_values(self, *attrs):
        values = []
        mtx = self.value_matrix(*attrs)
        for row in zip(*mtx):
            v = [ x for x in row if x ]
            values.append(' '.join(v))

        return values

    def is_empty(self, attr):
        """Return True if the field has no value present."""
        values = self.values(attr)
        return len(values) == 0

    def is_present(self, field):
        """Return True if the field has one or more values."""
        return not self.is_empty(field)

    def is_field_missing(self, attr):
        """Return True if the field is not on the description sheet."""
        return self.locus(attr) is None

    def is_required(self, attr):
        if self.fields.get(attr):
            return self.fields[attr].get('required', False)

    def is_optional(self, attr):
        return not self.is_required(attr)

    def is_file_list(self, attr):
        if self.fields.get(attr, None):
            return self.fields[attr].get('file_list', False)

    def values(self, attr):
        """Return all values for attr's field."""
        details = self.fields[attr]
        if details.get('cell_values') is None:
            if details.get('class'):
                details['cell_values'] = self._extract_virtual_values(details)
            else:
                details['cell_values'] = self._extract_values(attr)
        return details.get('cell_values')

    def paired_values(self, attr, other_attr):
        return self.value_matrix(attr, other_attr)

    def values_dict(self, *attrs):
        """Return a dict of filled value lists, one for each column in attrs
        and keyed by the corresponding attribute.  All lists will the
        same length, each list shorter than the longest list having
        been filled in with None.

        """
        matrix = self.value_matrix(*attrs)
        vdict = {}
        for i in xrange(len(attrs)):
            vdict[attrs[i]] = matrix[i]
        return vdict

    def value_matrix(self, *attrs):
        """Return a list containing a filled value list for each column in
        attrs; each list will have the same number of elements, lists
        shorter than the longest list having been filled in with None.

        """
        matrix = [ deepcopy(self.values(x)) for x in attrs ]
        max_len = len(max(matrix, key=lambda x: len(x)))
        for values in matrix:
            if len(values) < max_len:
                values.extend([ None ] * (max_len - len(values)))
        return matrix

    def field_name(self, attr):
        """Return the 'field_name' for attr's field."""
        if self.fields.get(attr):
            return self.fields[attr]['field_name']

    def locus(self, attr):
        """Return the header 'locus' for attr's field."""
        if self.fields.get(attr):
            return deepcopy(self.fields[attr].get('locus'))

    def value_list(self, attr):
        """If present, return the 'value_list' for attr's field."""
        if self.fields.get(attr):
            return self.fields[attr].get('value_list')

    def requirement(self, attr):
        """Return the 'require' value for attr's field."""
        if self.fields.get(attr):
            return self.fields[attr].get('required')

    def blank_rule(self, attr):
        """If present, return the 'blank' rule for attr's field."""
        if self.fields.get(attr):
            return self.fields[attr].get('blank')

    def repeating(self, attr):
        """Return the 'repeating' value for attr's field."""
        if self.fields.get(attr):
            return self.fields[attr].get('repeating')

    def data_type(self, attr):
        """Return the 'data_type' for attr's field."""
        if self.fields.get(attr):
            return self.fields[attr].get('data_type')

    def cell_address_for_value(self, attr, index):
        locus = self.locus(attr)
        if locus is None: return ''

        row = locus['row']
        col = locus['col']

        if self.heading_type == 'column':
            row += (self.data_offset + index)
        else:
            col += (self.data_offset + index)

        return self.cell_address(col, row)


    ######################################################################
    # _ methods
    ######################################################################

    def _add_error(self, attr, index, msg, error_list):
        address = self.cell_address_for_value(attr, index)
        msg = "[Sheet: %s - %s] %s" % (self.sheet_name, address, msg)
        error_list.append(msg)

    def _set_headings(self):
        """Find and set the headings locus for each field in config."""
        for attr in self.fields:
            details          = self.fields[attr]
            field_name       = details['field_name']
            locus            = self._find_heading_locus(field_name)
            details['locus'] = locus

    def _find_heading_locus(self, field_name):
        """Find the heading locus for 'field_name'. Field name is compared to
        cell values by normalizing both strings and comparing.
        Normalization removes all non-word characaters and converts
        the remaining characters to lower case.

        """
        if self._heading_column is not None:
            for row in xrange(1, self.HEADER_ROW_MAX + 1):
                if self._is_header_cell(col=self._heading_column, row=row, field_name=field_name):
                    return {'col': self._heading_column, 'row': row }
        elif self._heading_row is not None:
            for col in xrange(1, self.HEADER_COLUMN_MAX + 1):
                if self._is_header_cell(col=col, row=self._heading_row, field_name=field_name):
                    return {'col': col, 'row': self._heading_row}
        else:
            return self._brute_force_find_field(field_name)

    def _brute_force_find_field(self, field_name):
        for row in xrange(1, self.HEADER_ROW_MAX + 1):
            for col in xrange(1, self.HEADER_COLUMN_MAX + 1):
                if self._is_header_cell(col, row, field_name):
                    if self.heading_type == 'row':
                        self._heading_column = col
                    else:
                        self._heading_row = row

                    return {'col': col,'row': row }


    def _is_header_cell(self, col, row, field_name):
        cell = self.sheet.cell(column=col, row=row)
        value = cell.value if cell is not None else ''
        return self.normalize(value) == self.normalize(field_name)

    def _extract_virtual_values(self, details):
        cls = get_class(details.get('class'))
        obj = cls()
        return obj.values(self, details.get('arg_fields', []))

    def _extract_values(self, attr):
        """Based on the locus of attr's field's header."""
        if self.locus(attr) is None: return

        if self.heading_type.lower() == 'row':
            return self._extract_row(attr)
        else:
            return self._extract_column(attr)

    def _get_cell_value(self, cell):
        value = cell.value
        if value is None or unicode(value).strip() == '':
            value = None
        elif isinstance(value, basestring):
            value = self.fix_unicode(value)

        # Ugh, Microsoft.
        if isinstance(value, basestring) and value.startswith('=HYPERLINK'):
            value = value.split('"')[1]

        return value

    # TODO: Change extract column to stop after hitting blank cell
    # TODO: Have column comparisons check to see that columns are same len()
    def _extract_column(self, attr):
        if self.locus(attr) is None: return

        locus    = self.locus(attr)
        col      = locus['col']
        # read the first 20 columns past the heading locus
        data_row = locus['row'] + self.data_offset

        vals     = []
        for row in xrange(data_row, self._repeat_limit() + 1):
            cell = self.sheet.cell(column=col,row=row)
            val  = self._get_cell_value(cell)
            vals.append(val)

        return vals

    def _extract_row(self, attr):
        if self.locus(attr) is None: return

        locus   = self.locus(attr)
        row     = locus['row']
        # read the first 20 columns past the heading locus
        data_col = locus['col'] + self.data_offset


        vals = []
        for col in xrange(data_col, self._repeat_limit() + 1):
            cell = self.sheet.cell(column=col,row=row)
            val  = self._get_cell_value(cell)
            vals.append(val)

        # strip off trailing Nones
        while len(vals) > 0 and vals[-1] is None:
            del vals[-1]

        return vals

    def _values_quoted(self, attr, q='"'):
        return self._list_quoted(self.values(attr), q=q)

    def _list_quoted(self, strings, q='"'):
        return [ "%s%s%s" % (q,s,q) for s in strings ]

    def _do_type_validation(self, field, value, data_type):
        if data_type == 'year':
            if not self.is_valid_year(value):
                self.errors.append(self._format_error(field, value, data_type))
        elif data_type == 'uri':
            if not self.is_valid_uri(value):
                self.errors.append(self._format_error(field, value, data_type))
        elif data_type == 'lang':
            if not self.is_valid_lang(value):
                self.errors.append(self._format_error(field, value, data_type))
        elif data_type == 'email':
            if not self.is_valid_email(value):
                self.warnings.append(
                    self._format_error(field, value, data_type))
        elif data_type == 'integer':
            if not self.is_valid_integer(value):
                self.errors.append(
                    self._format_error(field, value, data_type))
        elif data_type == 'word':
            if not self.is_valid_word(value):
                self.errors.append(
                    self._format_error(field, value, data_type))
        elif data_type == 'string':
            pass
        else:
            raise OPennException('Unknown data type: "%s"' % (data_type,))

    def _format_error(self, field_name, value, data_type):
        return "%s is not a valid %s: %s" % (field_name, data_type, value)

    def _get_dups(self, values):
        vsorted = sorted(values)
        dups = []
        for g in itertools.groupby(sorted(values)):
            val = g[0]
            size = len(list(g[1]))
            if size > 1:
                dups.append((val,size))
        return dups

    def _repeat_limit(self):
        if self.__repeat_limit is None:
            repeat_config = self.repeat_limit

            if repeat_config is None:
                if self.heading_type.lower() == 'row':
                    return self.max_column
                else:
                    return self.max_row

            if repeat_config.get('fixed', None) is not None:
                return repeat_config.get('fixed')

            if repeat_config.get('fields', None) is not None:
                vals = []
                for attr in repeat_config.get('fields'):
                    vals.append(self._find_max_nonblank_index(attr))

                self.__repeat_limit = max(vals)

        return self.__repeat_limit

    def _find_max_nonblank_index(self, attr):
        max_field = 0

        lastval = ''
        locus = self.locus(attr)
        if self.heading_type.lower() == 'row':
            row = locus['row']
            data_col = locus['col'] + self.data_offset
            for col in xrange(data_col, self.max_column + 1):
                cell = self.sheet.cell(column=col, row=row)
                val = self._get_cell_value(cell)
                if val is None or unicode(val).strip() == '':
                    pass
                else:
                    max_field = col
                    lastval = val
        else:
            col = locus['col']
            data_row = locus['row'] + self.data_offset
            for row in xrange(data_row, self.max_row + 1):
                cell = self.sheet.cell(column=col, row=row)
                val = self._get_cell_value(cell)
                if val is None or unicode(val).strip() == '':
                    pass
                else:
                    max_field = row
                    lastval = val

        self.logger.info("Found last value '%s' for attr '%s' (row/col %d)", lastval, attr, max_field)

        return max_field
