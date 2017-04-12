# -*- coding: utf-8 -*-

import os
import sys
import json

from django.utils import unittest
from django.test import TestCase
from django.conf import settings

from openn.prep.op_workbook import OPWorkbook
from openn.prep.spreadsheet_xml import SpreadsheetXML
from openn.tests.helpers import *

class TestSpreadsheetXML(TestCase):
    this_dir                 = os.path.dirname(__file__)
    diaries_dir              = os.path.join(this_dir, 'data/diaries')
    sheets_dir               = os.path.join(this_dir, 'data/sheets')
    valid_workbook           = os.path.join(sheets_dir, 'valid_workbook.xlsx')
    unicode_workbook         = os.path.join(sheets_dir, 'unicode_workbook.xlsx')
    bibliophilly_workbook    = os.path.join(this_dir,
                                            'data/bibliophilly/FLPLewisE087/openn_metadata.xlsx')

    url1 = 'http://id.loc.gov/authorities/names/n50049445.html'
    url2 = 'http://id.loc.gov/authorities/subjects/sh99002320.html'
    url3 = 'http://id.loc.gov/authorities/subjects/sh85060757'
    url4 = 'http://id.loc.gov/authorities/subjects/sh2010118889'
    url5 = 'https://openpyxl.readthedocs.org/en/latest/api/openpyxl.worksheet.html?highlight=min_col#openpyxl.worksheet.worksheet.Worksheet.min_col'

    pacscl_diairies_json    = os.path.join(sheets_dir, 'pacscl_diaries.json')
    biblio_philly_json      = os.path.join(this_dir, '../bibliophilly.json')

    xml_config = [
        {
            'sheet_attr': 'pages',
            'sheet_root': 'pages',
            'field_groups': [
                {
                    'xml_attr': 'page',
                    'columns': [
                        'file_name', 'display_page', 'serial_num',
                        'tag1', 'value1', 'tag2', 'value2', 'tag3',
                        'value3', 'tag4', 'value4' ],
                },
            ]
        },
        {
            'sheet_attr': 'description',
            'sheet_root': 'description',
            'composite_fields': {
                'full_title': [
                    'repository_name',
                    'call_numberid',
                    'title',
                    'volume_number'
                ]
            },
            'field_groups': [
                {
                    'xml_attr': 'administrative',
                    'columns': [
                        'administrative_contact',
                        'administrative_contact_email'
                    ]
                },
                {
                    'xml_attr': 'metadata_creator',
                    'columns': [
                        'metadata_creator',
                        'metadata_creator_email'
                    ]
                },
                {
                    'xml_attr': 'identification',
                    'columns': [
                        'repository_city',
                        'repository_country',
                        'repository_name',
                        'source_collection',
                        'call_numberid',
                        'volume_number'
                    ],
                },
                {
                    'xml_attr': 'altId',
                    'columns': [
                        'alternate_id',
                        'alternate_id_type'
                    ],
                },
                {
                    'xml_attr': 'title',
                    'columns': [
                        'title',
                        'volume_number'
                    ],
                },
                {
                    'xml_attr': 'creator',
                    'columns': [
                        'creator_name',
                        'creator_uri'
                    ],
                },
                {
                    'xml_attr': 'origin',
                    'columns': [
                        'date_single',
                        'date_range_start',
                        'date_range_end',
                        'date_narrative',
                        'place_of_origin'
                    ],
                },
                {
                    'xml_attr': 'language',
                    'columns': [
                        'language',
                    ],
                },
                {
                    'xml_attr': 'page_info',
                    'columns': [
                        'page_count',
                        'page_gaps_in_images',
                    ],
                },
                {
                    'xml_attr': 'dimensions',
                    'columns': [
                        'page_dimensions',
                        'bound_dimensions',
                    ],
                },
                {
                    'xml_attr': 'related',
                    'columns': [
                        'related_resource',
                        'related_resource_url',
                    ],
                },
                {
                    'xml_attr': 'subjects',
                    'columns': [
                        'subject_names',
                        'subject_names_uri',
                    ],
                },
                {
                    'xml_attr': 'subjects_topical',
                    'columns': [
                        'subject_topical',
                        'subject_topical_uri',
                    ],
                },
                {
                    'xml_attr': 'subjects_geographic',
                    'columns': [
                        'subject_geographic',
                        'subject_geographic_uri',
                    ],
                },
                {
                    'xml_attr': 'subjects_genreform',
                    'columns': [
                        'subject_genreform',
                        'subject_genreform_uri',
                    ],
                },
                {
                    'xml_attr': 'image_rights',
                    'columns': [
                        'image_rights',
                        'image_copyright_holder',
                        'image_copyright_year',
                    ],
                },
                {
                    'xml_attr': 'metadata_rights',
                    'columns': [
                        'metadata_rights',
                        'metadata_copyright_holder',
                        'metadata_copyright_year',
                    ],
                },


            ]
        }
    ]

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def get_config(self):
        return json.load(open(self.pacscl_diairies_json))

    def test_init(self):
        self.assertIsInstance(SpreadsheetXML(settings.LICENSES), SpreadsheetXML)

    def test_run(self):
        config = self.get_config()
        workbook = OPWorkbook(self.valid_workbook, config)
        sp_xml = SpreadsheetXML(settings.LICENSES)

        xml = sp_xml.build_xml(workbook.data(), config['xml_config'])

    def test_unicode(self):
        config = self.get_config()
        workbook = OPWorkbook(self.unicode_workbook, config)
        sp_xml = SpreadsheetXML(settings.LICENSES)

        xml = sp_xml.build_xml(workbook.data(), config['xml_config'])

    def test_biblio_philly(self):
        config = json.load(open(self.biblio_philly_json))
        workbook = OPWorkbook(self.bibliophilly_workbook, config)
        sp_xml = SpreadsheetXML(settings.LICENSES)

        xml = sp_xml.build_xml(workbook.data(), config['xml_config'])
        print xml
