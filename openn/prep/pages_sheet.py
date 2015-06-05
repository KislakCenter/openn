#!/usr/bin/env python
# -*- coding: utf-8 -*-

from openn.prep.validatable_sheet import ValidatableSheet

class PagesSheet(ValidatableSheet):

    ######################################################################
    # Instance methods
    ######################################################################

    def __init__(self, op_workbook, config={}):
        super(PagesSheet, self).__init__(op_workbook, config)

    # --------------------------------------------------------------------
    # Validation
    # --------------------------------------------------------------------

    def validate(self):
        self.check_required_headings()
        self.check_pages_values()
        self.validate_file_list(
            'file_name', self.op_workbook.workbook_dir, allow_blank=False)

    def check_required_headings(self):
        for field in self.required_fields:
            if not field['locus']:
                msg = 'Required field is missing: %s' % (field['field_name'],)
                self.errors.append(msg)

    def check_pages_values(self):
        for attr in self.fields:
            self.validate_field(attr)
