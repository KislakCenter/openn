#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json

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

    # Field 1
    # Empty if field 1 empty (invalid)
    # Empty if field 1 empty (valid)

    # Field 2 (repeating)
    # Empty if field 2 nonempty (first and third present)

    # Field 3
    # Empty if 3 is CAT (valid)
    # Empty if 3 is CAT (invalid)

    # Field 4 (cat is lower case)
    # Empty if field 4 is CAT (valid)

    # Field 5 (repeating)
    # Empty if 5 is CAT
    empty_if_workbook = os.path.join(sheets_dir, 'empty_if.xlsx')

    # Date (single)
    # Date (range) start
    # Date (range) end
    # Image copyright holder
    # Image copyright year
    # Alternate ID type
    invalid_nonblanks        = os.path.join(sheets_dir, 'invalid_values_should_be_blank.xlsx')

    valid_workbook           = os.path.join(sheets_dir, 'valid_workbook.xlsx')
    value_lists_workbook     = os.path.join(sheets_dir, 'value_lists.xlsx')
    repeating_workbook       = os.path.join(sheets_dir, 'repeating_and_nonrepeating.xlsx')
    missing_field_workbook   = os.path.join(sheets_dir, 'missing_optional_fields.xlsx')

    pacscl_diairies_json    = os.path.join(sheets_dir, 'pacscl_diaries.json')
    value_lists_test_config = json.load(open(os.path.join(sheets_dir, 'value_lists_config.json')))
    repeating_config        = json.load(open(os.path.join(sheets_dir, 'repeating_config.json')))
    field_missing_config    = json.load(open(os.path.join(sheets_dir, 'field_missing_config.json')))
    requirements_config     = json.load(open(os.path.join(sheets_dir, 'requirements_config.json')))
    empty_if_config         = json.load(open(os.path.join(sheets_dir, 'empty_if_config.json')))

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def get_config(self):
        return json.load(open(self.pacscl_diairies_json))

    def test_init(self):
        sheet = OPWorkbook(self.valid_workbook, self.get_config()).description
        self.assertIsInstance(sheet, ValidatableSheet)

    # Field 1
    # Required if field 1 empty (invalid)
    def test_validate_required_if_other_empty_invalid(self):
        sheet = OPWorkbook(self.required_values_workbook, self.requirements_config).description
        sheet.validate_requirement('required_if_field_1_empty_invalid')
        self.assertEqual(len(sheet.errors), 1)
        self.assertRegexpMatches(sheet.errors[0], r'Required if field 1.* cannot be empty.*Field 1')

    # Field 1
    # Required if field 1 empty (valid)
    def test_validate_required_if_other_empty_valid(self):
        sheet = OPWorkbook(self.required_values_workbook, self.requirements_config).description
        sheet.validate_requirement('required_if_field_1_empty_valid')
        self.assertEqual(len(sheet.errors), 0)

    # Field 2 (repeating)
    # Required if field 2 nonempty (first and third missing)
    def test_validate_required_if_other_empty_valid_repeating(self):
        sheet = OPWorkbook(self.required_values_workbook, self.requirements_config).description
        sheet.validate_requirement('required_if_field_2_nonempty_first_and_third_missing')
        self.assertEqual(len(sheet.errors), 2)

    # Field 3 (required, invalid)
    def test_validate_requirement_invalid(self):
        sheet = OPWorkbook(self.required_values_workbook, self.requirements_config).description
        sheet.validate_requirement('field_3_required_invalid')
        self.assertEqual(len(sheet.errors), 1)
        self.assertRegexpMatches(sheet.errors[0], r'Field 3.* cannot be empty')

    # Field 4 (required, valid)
    def test_validate_requirement_valid(self):
        sheet = OPWorkbook(self.required_values_workbook, self.requirements_config).description
        sheet.validate_requirement('field_4_required_valid')
        self.assertEqual(len(sheet.errors), 0)

    # Field 5 (not required, no value)
    def test_validate_requirement_not_required_no_value(self):
        sheet = OPWorkbook(self.required_values_workbook, self.requirements_config).description
        sheet.validate_requirement('field_5_not_required_no_value')
        self.assertEqual(len(sheet.errors), 0)

    # Field 6 (not required, value)
    def test_validate_requirement_not_required_with_value(self):
        sheet = OPWorkbook(self.required_values_workbook, self.requirements_config).description
        sheet.validate_requirement('field_6_not_required_value')
        self.assertEqual(len(sheet.errors), 0)

    # Field 7
    # Required if 7 is CAT (valid)
    def test_validate_required_if_other_in_list_valid(self):
        sheet = OPWorkbook(self.required_values_workbook, self.requirements_config).description
        sheet.validate_requirement('required_if_7_is_CAT_valid')
        self.assertEqual(len(sheet.errors), 0)
    # Field 7
    # Required if 7 is CAT (invalid)
    def test_validate_required_if_other_in_list_invalid(self):
        sheet = OPWorkbook(self.required_values_workbook, self.requirements_config).description
        sheet.validate_requirement('required_if_7_is_CAT_invalid')
        self.assertEqual(len(sheet.errors), 1)
        self.assertRegexpMatches(sheet.errors[0], r'Required.* cannot be empty.*if.*CAT')

    # Field 8 (cat is lower case)
    # Require if field 8 is CAT (valid)
    def test_validate_required_if_other_in_list_differing_case(self):
        sheet = OPWorkbook(self.required_values_workbook, self.requirements_config).description
        sheet.validate_requirement('require_if_field_8_is_CAT_valid')
        self.assertEqual(len(sheet.errors), 0)

    # Field 9 (repeating)
    # Required if 9 is CAT
    def test_validate_required_if_other_in_list_repeating(self):
        sheet = OPWorkbook(self.required_values_workbook, self.requirements_config).description
        sheet.validate_requirement('required_if_9_is_CAT')
        self.assertEqual(len(sheet.errors), 1)
        self.assertRegexpMatches(sheet.errors[0], r'Required.* cannot be empty.*if.*CAT')

    # Field 2 (repeating)
    # Empty if field 2 nonempty (first and third present)
    def test_validate_blank_if_other_nonempty_invalid(self):
        sheet = OPWorkbook(self.empty_if_workbook, self.empty_if_config).description
        sheet.validate_blank('empty_if_field_2_nonempty_first_and_third_present')
        self.assertEqual(len(sheet.errors), 2)
        self.assertRegexpMatches(sheet.errors[0], r'.* must be empty if.*has a value; found')
        self.assertRegexpMatches(sheet.errors[1], r'.* must be empty if.*has a value; found')

    # Field 1
    # Empty if field 1 empty (invalid)
    def test_validate_blank_if_other_empty_invalid(self):
        sheet = OPWorkbook(self.empty_if_workbook, self.empty_if_config).description
        sheet.validate_blank('empty_if_field_1_empty_invalid')
        self.assertEqual(len(sheet.errors), 1)
        self.assertRegexpMatches(sheet.errors[0], r'.* must be empty if.*is empty; found.*')

    # Field 1
    # Empty if field 1 empty (valid)
    def test_validate_blank_if_other_empty_valid(self):
        sheet = OPWorkbook(self.empty_if_workbook, self.empty_if_config).description
        sheet.validate_blank('empty_if_field_1_empty_valid')
        self.assertEqual(len(sheet.errors), 0)


    # Field 3
    # Empty if 3 is CAT (invalid)
    def test_validate_blank_if_other_in_list_invalid(self):
        sheet = OPWorkbook(self.empty_if_workbook, self.empty_if_config).description
        sheet.validate_blank('empty_if_3_is_cat_invalid')
        self.assertEqual(len(sheet.errors), 1)
        self.assertRegexpMatches(sheet.errors[0], r'.* must be empty if.*is.*CAT.*; found:')

    # Field 3
    # Empty if 3 is CAT (valid)
    def test_validate_blank_if_other_in_list_valid(self):
        sheet = OPWorkbook(self.empty_if_workbook, self.empty_if_config).description
        sheet.validate_blank('empty_if_3_is_cat_valid')
        self.assertEqual(len(sheet.errors), 0)

    # Field 4 (cat is lower case)
    # Empty if field 4 is CAT (invalid)
    def test_validate_blank_if_other_in_list_case_insensitive_invalid(self):
        sheet = OPWorkbook(self.empty_if_workbook, self.empty_if_config).description
        sheet.validate_blank('empty_if_field_4_is_cat_invalid')
        self.assertEqual(len(sheet.errors), 1)
        self.assertRegexpMatches(sheet.errors[0], r'.* must be empty if.*is.*cat.*; found:')

    # Field 5 (repeating)
    # Empty if 5 is CAT
    def test_validate_blank_if_other_in_list_repeating(self):
        sheet = OPWorkbook(self.empty_if_workbook, self.empty_if_config).description
        sheet.validate_blank('empty_if_5_is_cat')
        self.assertEqual(len(sheet.errors), 1)
        self.assertRegexpMatches(sheet.errors[0], r'.* must be empty if.*is.*CAT.*; found:.*value 2.*')

    # Rights PD
    def test_validate_value_list_valid(self):
        sheet = OPWorkbook(self.value_lists_workbook, self.value_lists_test_config).description
        sheet.validate_value_list('rights_pd')
        self.assertEqual(len(sheet.errors), 0)

    # Rights CC-X (not in list)
    def test_validate_value_list_invalid(self):
        sheet = OPWorkbook(self.value_lists_workbook, self.value_lists_test_config).description
        sheet.validate_value_list('rights_cc_x_not_in_list')
        self.assertEqual(len(sheet.errors), 1)
        self.assertRegexpMatches(sheet.errors[0], r'Rights CC-X.*not valid.*expected.*')

    # Rights 4 (empty)
    def test_validate_value_list_with_value_empty(self):
        sheet = OPWorkbook(self.value_lists_workbook, self.value_lists_test_config).description
        sheet.validate_value_list('rights_4_blank')
        self.assertEqual(len(sheet.errors), 0)

    # Rights PD with space
    def test_validate_value_list_valid_value_plus_space(self):
        sheet = OPWorkbook(self.value_lists_workbook, self.value_lists_test_config).description
        sheet.validate_value_list('rights_pd_with_space')
        self.assertEqual(len(sheet.errors), 0)

    # Rights PD with space
    def test_validate_value_list_valid_value_lower_case(self):
        sheet = OPWorkbook(self.value_lists_workbook, self.value_lists_test_config).description
        sheet.validate_value_list('rights_pd_lower_case')
        self.assertEqual(len(sheet.errors), 0)

    def test_validate_repeating_false_one_value(self):
        sheet = OPWorkbook(self.repeating_workbook, self.repeating_config).description
        sheet.validate_repeating('non_repeating_field_valid')
        self.assertEqual(len(sheet.errors), 0)

    def test_validate_repeating_false_more_than_one_value(self):
        sheet = OPWorkbook(self.repeating_workbook, self.repeating_config).description
        sheet.validate_repeating('non_repeating_field_invalid')
        self.assertEqual(len(sheet.errors), 1)
        self.assertRegexpMatches(sheet.errors[0], r'More than one.*Non-repeating field invalid.*value1.*value2')

    def test_validate_repeating_true_one_value(self):
        sheet = OPWorkbook(self.repeating_workbook, self.repeating_config).description
        sheet.validate_repeating('repeating_field_one_value')
        self.assertEqual(len(sheet.errors), 0)

    def test_validate_repeating_true_more_than_one_value(self):
        sheet = OPWorkbook(self.repeating_workbook, self.repeating_config).description
        sheet.validate_repeating('repeating_field_multiple_values')
        self.assertEqual(len(sheet.errors), 0)

    def test_validate_sheet_missing_optional_fields(self):
        sheet = OPWorkbook(self.missing_field_workbook, self.field_missing_config).description
        sheet.validate()
        self.assertFalse(sheet.has_errors())
