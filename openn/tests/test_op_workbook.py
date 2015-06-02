#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from django.utils import unittest
from django.test import TestCase
from django.conf import settings
from django.core.exceptions import ValidationError

from openn.prep.op_workbook import OPWorkbook

class TestOPWorkbook(TestCase):
    this_dir                = os.path.dirname(__file__)
    diaries_dir             = os.path.join(this_dir, 'data/diaries')
    sheets_dir              = os.path.join(this_dir, 'data/sheets')

    # Date (range) end
    # Place of origin
    # Metadata copyright year
    # Alternate ID type
    invalid_missing_required = os.path.join(sheets_dir, 'invalid_missing_required.xlsx')

    # Date (single)
    # Date (range) start
    # Date (range) end
    # Image copyright holder
    # Image copyright year
    # Alternate ID type
    invalid_nonblanks        = os.path.join(sheets_dir, 'invalid_values_should_be_blank.xlsx')

    value_lists_workbook     = os.path.join(sheets_dir, 'value_lists.xlsx')
    repeating_workbook       = os.path.join(sheets_dir, 'repeating_and_nonrepeating.xlsx')
    missing_field_workbook    = os.path.join(sheets_dir, 'missing_optional_fields.xlsx')

    helen_griffith           = os.path.join(diaries_dir, 'bryn_mawr/HelenGriffith_Diary.xlsx')
    mary_ayer                = os.path.join(diaries_dir, 'bryn_mawr/MaryAyer_Diary.xlsx')
    mww_diary_vol10          = os.path.join(diaries_dir, 'bryn_mawr/MWW_Diary_Vol10.xlsx')
    mww_diary_vol11          = os.path.join(diaries_dir, 'bryn_mawr/MWW_Diary_Vol11.xlsx')
    mww_diary_vol12          = os.path.join(diaries_dir, 'bryn_mawr/MWW_Diary_Vol12.xlsx')
    mww_diary_vol9           = os.path.join(diaries_dir, 'bryn_mawr/MWW_Diary_Vol9.xlsx')
    pacscl_coates_sharpless  = os.path.join(diaries_dir, 'haverford/Account of Coates, Shapless, etc/PACSCL metadata.xlsx')
    william_allinson_v1      = os.path.join(diaries_dir, 'haverford/Allinson, William/PACSCL metadata v1.xlsx')
    william_allinson_v2      = os.path.join(diaries_dir, 'haverford/Allinson, William/PACSCL metadata v2.xlsx')
    william_allinson_v3      = os.path.join(diaries_dir, 'haverford/Allinson, William/PACSCL metadata v3.xlsx')
    david_bacon              = os.path.join(diaries_dir, 'haverford/Bacon, David/PACSCL metadata.xlsx')
    joseph_sampson           = os.path.join(diaries_dir, 'haverford/Sansom, Joseph/PACSCL metadata.xlsx')
    swayne                   = os.path.join(diaries_dir, 'haverford/Swayne/PACSCL metadata.xlsx')
    xls_cooper               = os.path.join(diaries_dir, 'swarthmore/Cooper/PACSCL_Cooper.xls')
    xls_pierce               = os.path.join(diaries_dir, 'swarthmore/Pierce/PACSCL_Pierce.xls')
    xls_sharpless            = os.path.join(diaries_dir, 'swarthmore/Sharpless/PACSCL_Sharpless.xls')

    url1 = 'http://id.loc.gov/authorities/names/n50049445.html'
    url2 = 'http://id.loc.gov/authorities/subjects/sh99002320.html'
    url3 = 'http://id.loc.gov/authorities/subjects/sh85060757'
    url4 = 'http://id.loc.gov/authorities/subjects/sh2010118889'
    url5 = 'https://openpyxl.readthedocs.org/en/latest/api/openpyxl.worksheet.html?highlight=min_col#openpyxl.worksheet.worksheet.Worksheet.min_col'

    value_lists_test_config = {
        'description' : {
            'sheet_name': 'Description',
            'data_offset': 2,
            'heading_type': 'row',
            'fields': {
                'rights_pd' : {
                    'field_name': 'Rights PD',
                    'required' : True,
                    'repeating' : False,
                    'data_type' : 'string',
                    'value_list': [ 'CC-BY', 'CC0', 'PD' ]
                },
                'rights_cc_by': {
                    'field_name': 'Rights CC-BY',
                    'required': True,
                    'repeating': False,
                    'data_type': 'string',
                    'value_list': [ 'CC-BY', 'CC0', 'PD' ]
                },
                'rights_cc_x_not_in_list': {
                    'field_name': 'Rights CC-X (not in list)',
                    'required': True,
                    'repeating': False,
                    'data_type': 'string',
                    'value_list': [ 'CC-BY', 'CC0', 'PD' ]
                },
                'rights_4_blank': {
                    'field_name': 'Rights 4 (blank)',
                    'required': True,
                    'repeating': False,
                    'data_type': 'string',
                    'value_list': [ 'CC-BY', 'CC0', 'PD' ]
                },
                'rights_pd_with_space': {
                    'field_name': 'Rights PD with space',
                    'required': True,
                    'repeating': False,
                    'data_type': 'string',
                    'value_list': [ 'CC-BY', 'CC0', 'PD' ]
                }
            }
        }
    }

    repeating_config = {
        'description' : {
            'sheet_name': 'Description',
            'data_offset': 2,
            'heading_type': 'row',
            'fields': {
                'non_repeating_field_valid': {
                    'field_name': 'Non-repeating field valid',
                    'required': True,
                    'repeating': False,
                    'data_type': 'string'
                },
                'non_repeating_field_invalid': {
                    'field_name': 'Non-repeating field invalid',
                    'required': True,
                    'repeating': False,
                    'data_type': 'string'
                },
                'repeating_field_one_value': {
                    'field_name': 'Repeating field one value',
                    'required': True,
                    'repeating': True,
                    'data_type': 'string'
                },
                'repeating_field_multiple_values': {
                    'field_name': 'Repeating field multiple values',
                    'required': True,
                    'repeating': True,
                    'data_type': 'string'
                }
            }
        }
    }

    field_missing_config = {
        'description' : {
            'sheet_name': 'Description',
            'data_offset': 2,
            'heading_type': 'row',
            'fields' : {
                'field1': {
                    'field_name': 'Field1',
                    'required': False,
                    'repeating': True,
                    'data_type': 'string'
                },
                'field2': {
                    'field_name': 'Field2',
                    'required': False,
                    'repeating': True,
                    'data_type': 'string'
                },
                'field3': {
                    'field_name': 'Field3',
                    'required': False,
                    'repeating': True,
                    'data_type': 'string'
                },
                'field4': {
                    'field_name': 'Field4',
                    'required': False,
                    'repeating': True,
                    'data_type': 'string'
                },
                'field5': {
                    'field_name': 'Field5',
                    'required': False,
                    'repeating': True,
                    'data_type': 'string'
                }
            }
        }
    }

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def get_config(self):
        return settings.SPREADSHEET_CONFIG

    def test_init(self):
        sheet = OPWorkbook(self.helen_griffith, self.get_config())
        self.assertIsInstance(sheet,OPWorkbook)

    def test_validate_description(self):
        sheet = OPWorkbook(self.helen_griffith, self.get_config())
        sheet.validate_description()
        self.assertFalse(sheet.has_description_errors())

    def test_validate_sheet_missing_optional_fields(self):
        sheet = OPWorkbook(self.missing_field_workbook, self.field_missing_config)
        sheet.validate_description()
        self.assertFalse(sheet.has_description_errors())

if __name__ == '__main__':
    unittest2.main()
