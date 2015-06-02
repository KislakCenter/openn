#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from django.utils import unittest
from django.test import TestCase
from django.conf import settings
from django.core.exceptions import ValidationError

from openn.prep.op_workbook import OPWorkbook
from openn.prep.description_sheet import DescriptionSheet
from openn.prep.validatable_sheet import ValidatableSheet

class TestDescriptionSheet(TestCase):
    this_dir                 = os.path.dirname(__file__)
    diaries_dir              = os.path.join(this_dir, 'data/diaries')
    sheets_dir               = os.path.join(this_dir, 'data/sheets')

    # Field 1
    # Required if field 1 empty (invalid)
    # Required if field 1 empty (valid)
    #
    # Field 2 (repeating)
    # Required if field 2 nonempty (first and third missing)
    #
    # Field 3 (required, invalid)
    # Field 4 (required, valid)
    # Field 5 (not required, no value)
    # Field 6 (not required, value)
    required_values_workbook = os.path.join(sheets_dir, 'required_values.xlsx')

    # Date (single)
    # Date (range) start
    # Date (range) end
    # Image copyright holder
    # Image copyright year
    # Alternate ID type
    invalid_nonblanks        = os.path.join(sheets_dir, 'invalid_values_should_be_blank.xlsx')

    value_lists_workbook     = os.path.join(sheets_dir, 'value_lists.xlsx')
    repeating_workbook       = os.path.join(sheets_dir, 'repeating_and_nonrepeating.xlsx')
    missing_field_workbook   = os.path.join(sheets_dir, 'missing_optional_fields.xlsx')

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

    requirements_config = {
        'description': {
            'sheet_name': 'Description',
            'heading_type': 'row',
            'data_offset': 2,
            'fields': {
                'field_1': {
                    'field_name': 'Field 1',
                    'required': False,
                    'repeating': False,
                    'data_type': 'string'
                },
                'required_if_field_1_empty_invalid': {
                    'field_name': 'Required if field 1 empty (invalid)',
                    'required': {
                        'if': {
                            'field': 'field_1',
                            'is': 'EMPTY'
                        }
                    },
                    'repeating': False,
                    'data_type': 'string'
                },
                'required_if_field_1_empty_valid': {
                    'field_name': 'Required if field 1 empty (valid)',
                    'required': {
                        'if': {
                            'field': 'field_1',
                            'is': 'EMPTY'
                        }
                    },
                    'repeating': True,
                    'data_type': 'string'
                },
                'field_2_repeating': {
                    'field_name': 'Field 2 (repeating)',
                    'required': False,
                    'repeating': True,
                    'data_type': 'string'
                },
                'required_if_field_2_nonempty_first_and_third_missing': {
                    'field_name': 'Required if field 2 nonempty (first and third missing)',
                    'required': {
                        'if': {
                            'field': 'field_2_repeating',
                            'is': 'NONEMPTY'
                        }
                    },
                    'repeating': True,
                    'data_type': 'string'
                },
                'field_3_required_invalid': {
                    'field_name': 'Field 3 (required, invalid)',
                    'required': True,
                    'repeating': True,
                    'data_type': 'string'
                },
                'field_4_required_valid': {
                    'field_name': 'Field 4 (required, valid)',
                    'required': True,
                    'repeating': True,
                    'data_type': 'string'
                },
                'field_5_not_required_no_value': {
                    'field_name': 'Field 5 (not required, no value)',
                    'required': False,
                    'repeating': True,
                    'data_type': 'string'
                },
                'field_6_not_required_value': {
                    'field_name': 'Field 6 (not required, value)',
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
        sheet = OPWorkbook(self.helen_griffith, self.get_config()).description
        self.assertIsInstance(sheet, DescriptionSheet)
        self.assertIsInstance(sheet, ValidatableSheet)

    # Field 1
    # Required if field 1 empty (invalid)
    def test_required_with_blank_error(self):
        sheet = OPWorkbook(self.required_values_workbook, self.requirements_config).description
        sheet.validate_requirement('required_if_field_1_empty_invalid')
        self.assertEqual(len(sheet.errors), 1)
        self.assertRegexpMatches(sheet.errors[0], r'Required if field 1.* cannot be empty.*Field 1')

    # Field 1
    # Required if field 1 empty (valid)
    def test_required_with_blank_valid(self):
        sheet = OPWorkbook(self.required_values_workbook, self.requirements_config).description
        sheet.validate_requirement('required_if_field_1_empty_valid')
        self.assertEqual(len(sheet.errors), 0)

    #
    # Field 2 (repeating)
    # Required if field 2 nonempty (first and third missing)
    def test_required_with_value_repeating(self):
        sheet = OPWorkbook(self.required_values_workbook, self.requirements_config).description
        sheet.validate_requirement('required_if_field_2_nonempty_first_and_third_missing')
        self.assertEqual(len(sheet.errors), 2)

    # Field 3 (required, invalid)
    def test_required_field_error(self):
        sheet = OPWorkbook(self.required_values_workbook, self.requirements_config).description
        sheet.validate_requirement('field_3_required_invalid')
        self.assertEqual(len(sheet.errors), 1)
        self.assertRegexpMatches(sheet.errors[0], r'Field 3.* cannot be empty')

    # Field 4 (required, valid)
    # Field 5 (not required, no value)
    # Field 6 (not required, value)

    # Date (single)
    def test_must_be_empty_with_nonempty_error(self):
        sheet = OPWorkbook(self.invalid_nonblanks, self.get_config()).description
        sheet.validate_blank('date_single')
        self.assertEqual(len(sheet.errors), 1)
        self.assertRegexpMatches(sheet.errors[0], r'Date \(single\).* must be empty.*start')

    # Date (range) start
    def test_must_be_empty_with_nonempty_error2(self):
        sheet = OPWorkbook(self.invalid_nonblanks, self.get_config()).description
        sheet.validate_blank('date_range_start')
        self.assertEqual(len(sheet.errors), 1)
        self.assertRegexpMatches(sheet.errors[0], r'Date \(range\) start.* must be empty.*single')

    # Image copyright holder
    def test_must_be_empty_with_value_error(self):
        sheet = OPWorkbook(self.invalid_nonblanks, self.get_config()).description
        sheet.validate_blank('image_copyright_holder')
        self.assertEqual(len(sheet.errors), 1)
        self.assertRegexpMatches(sheet.errors[0], r'Image copyright holder.* must be empty.*PD')

    # Alternate ID type
    def test_must_be_empty_with_empty_error(self):
        sheet = OPWorkbook(self.invalid_nonblanks, self.get_config()).description
        sheet.validate_blank('alternate_id_type')
        self.assertEqual(len(sheet.errors), 1)
        self.assertRegexpMatches(sheet.errors[0], r'Alternate ID type.* must be empty.*Alternate ID.*empty')

    # Rights PD
    def test_value_list_valid(self):
        sheet = OPWorkbook(self.value_lists_workbook, self.value_lists_test_config).description
        sheet.validate_value_list('rights_pd')
        self.assertEqual(len(sheet.errors), 0)

    # Rights CC-X (not in list)
    def test_value_list_value_not_in_list(self):
        sheet = OPWorkbook(self.value_lists_workbook, self.value_lists_test_config).description
        sheet.validate_value_list('rights_cc_x_not_in_list')
        self.assertEqual(len(sheet.errors), 1)
        self.assertRegexpMatches(sheet.errors[0], r'Rights CC-X.*not valid.*expected.*')

    # Rights 4 (empty)
    def test_value_list_with_value_empty(self):
        sheet = OPWorkbook(self.value_lists_workbook, self.value_lists_test_config).description
        sheet.validate_value_list('rights_4_blank')
        self.assertEqual(len(sheet.errors), 0)

    # Rights PD with space
    def test_value_list_valid_value_plus_space(self):
        sheet = OPWorkbook(self.value_lists_workbook, self.value_lists_test_config).description
        sheet.validate_value_list('rights_pd_with_space')
        self.assertEqual(len(sheet.errors), 1)
        self.assertRegexpMatches(sheet.errors[0], r'Rights PD with space.*"PD ".*not valid.*expected.*')

    def test_repeating_false_one_value(self):
        sheet = OPWorkbook(self.repeating_workbook, self.repeating_config).description
        sheet.validate_repeating('non_repeating_field_valid')
        self.assertEqual(len(sheet.errors), 0)

    def test_repeating_false_more_than_one_value(self):
        sheet = OPWorkbook(self.repeating_workbook, self.repeating_config).description
        sheet.validate_repeating('non_repeating_field_invalid')
        self.assertEqual(len(sheet.errors), 1)
        self.assertRegexpMatches(sheet.errors[0], r'More than one.*Non-repeating field invalid.*value1.*value2')

    def test_repeating_true_one_value(self):
        sheet = OPWorkbook(self.repeating_workbook, self.repeating_config).description
        sheet.validate_repeating('repeating_field_one_value')
        self.assertEqual(len(sheet.errors), 0)

    def test_repeating_true_more_than_one_value(self):
        sheet = OPWorkbook(self.repeating_workbook, self.repeating_config).description
        sheet.validate_repeating('repeating_field_multiple_values')
        self.assertEqual(len(sheet.errors), 0)

    def test_is_valid_uri(self):
        for url in [ self.url1, self.url2, self.url3, self.url4, self.url5 ]:
            self.assertTrue(ValidatableSheet.is_valid_uri(url))

    def test_is_not_valid_uri(self):
        self.assertFalse(ValidatableSheet.is_valid_uri("car money"))

    def test_is_valid_year(self):
        for year in (2013, 013, 3000, -5000, 2):
            self.assertTrue(ValidatableSheet.is_valid_year(year), ("%d should be a valid year" % (year,)))

    def test_is_not_valid_year(self):
        for year in (2013.3, 'car', 3001, -5001):
            self.assertFalse(ValidatableSheet.is_valid_year(year), ("%s should not be a valid year" % (str(year),)))

    def test_is_valid_email(self):
        self.assertTrue(ValidatableSheet.is_valid_email('joe@example.com'))

    def test_is_valid_lang(self):
        for x in ('eng', 'eng ', ' eng ', 'en'):
            self.assertTrue(ValidatableSheet.is_valid_lang(x), ('%s should be a valid lang' % x))

    def test_is_not_valid_lang(self):
        for x in ('engx', 'x ', ' e ', 'enx'):
            self.assertFalse(ValidatableSheet.is_valid_lang(x), ('%s should not be a valid lang' % x))