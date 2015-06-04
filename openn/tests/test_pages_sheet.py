#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import pprint

from django.utils import unittest
from django.test import TestCase
from django.conf import settings
from django.core.exceptions import ValidationError

from openn.prep.op_workbook import OPWorkbook
from openn.prep.pages_sheet import PagesSheet
from openn.prep.validatable_sheet import ValidatableSheet

class TestPagesSheet(TestCase):
    this_dir                 = os.path.dirname(__file__)
    diaries_dir              = os.path.join(this_dir, 'data/diaries')
    sheets_dir               = os.path.join(this_dir, 'data/sheets')

    helen_griffith_workbook  = os.path.join(diaries_dir, 'bryn_mawr/HelenGriffith_Diary.xlsx')
    pages_workbook           = os.path.join(sheets_dir, 'pages.xlsx')

    pages_config = {
        'description': {
            'sheet_name': 'Description',
            'data_offset': 2,
            'heading_type': 'row', # headings on left, data read left-to-right
            'fields': { }
        },
        'pages': {
            'sheet_name': 'Pages',
            'data_offset': 1,
            'heading_type': 'column',
            'fields': {
                'object_id': {
                    'field_name': 'OBJECT_ID',
                    'required': False,
                    'repeating': True,
                    'data_type': 'string'
                },
                'serial_num': {
                    'field_name': 'SERIAL_NUM',
                    'repeating': True,
                    'data_type': 'integer',
                    'required': {
                        'if': {
                            'field': 'file_name',
                            'is': 'NONEMPTY'
                        }
                    },
                    'blank': {
                        'if': {
                            'field': 'file_name',
                            'is': 'EMPTY'
                        }
                    }
                },
                'display_page': {
                    'field_name': 'DISPLAY PAGE',
                    'required': {
                        'if': {
                            'field': 'file_name',
                            'is': 'NONEMPTY'
                        }
                    },
                    'repeating': True,
                    'data_type': 'string',
                    'blank': {
                        'if': {
                            'field': 'file_name',
                            'is': 'EMPTY'
                        }
                    }
                },
                'file_name': {
                    'field_name': 'FILE_NAME',
                    'required': True,   # Must have at least one file name
                    'repeating': True,
                    'data_type': 'string'
                },
                'tag1': {
                    'field_name': 'TAG1',
                    'required': False,
                    'repeating': True,
                    'data_type': 'string',
                    'blank': {
                        'if': {
                            'field': 'file_name',
                            'is': 'EMPTY'
                        }
                    }
                },
                'value1': {
                    'field_name': 'VALUE1',
                    'required': {
                        'if': {
                            'field': 'tag1',
                            'is': [ 'TOC1', 'TOC2', 'TOC3', 'ILL' ]
                        }
                     },
                     'blank': {
                         'if': {
                             'field': 'tag1',
                             'is': 'EMPTY'
                         }
                     },
                     'repeating': True,
                    'data_type': 'string'
                },
                'tag2': {
                    'field_name': 'TAG2',
                    'required': False,
                    'repeating': True,
                    'data_type': 'string',
                    'blank': {
                        'if': {
                            'field': 'file_name',
                            'is': 'EMPTY'
                        }
                    }
                },
                'value2': {
                    'field_name': 'VALUE2',
                    'required': {
                        'if': {
                            'field': 'tag2',
                            'is': [ 'TOC1', 'TOC2', 'TOC3', 'ILL' ]
                        }
                     },
                     'blank': {
                         'if': {
                             'field': 'tag2',
                             'is': 'EMPTY'
                         }
                     },
                     'repeating': True,
                    'data_type': 'string'
                },
                'tag3': {
                    'field_name': 'TAG3',
                    'required': False,
                    'repeating': True,
                    'data_type': 'string',
                    'blank': {
                        'if': {
                            'field': 'file_name',
                            'is': 'EMPTY'
                        }
                    }
                },
                'value3': {
                    'field_name': 'VALUE3',
                    'required': {
                        'if': {
                            'field': 'tag3',
                            'is': [ 'TOC1', 'TOC2', 'TOC3', 'ILL' ]
                        }
                    },
                    'blank': {
                        'if': {
                            'field': 'tag3',
                            'is': 'EMPTY'
                        }
                    },
                    'repeating': True,
                    'data_type': 'string'
                },
                'tag4': {
                    'field_name': 'TAG4',
                    'required': False,
                    'repeating': True,
                    'data_type': 'string',
                    'blank': {
                        'if': {
                            'field': 'file_name',
                            'is': 'EMPTY'
                        }
                    }
                },
                'value4': {
                    'field_name': 'VALUE4',
                    'required': {
                        'if': {
                            'field': 'tag4',
                            'is': [ 'TOC1', 'TOC2', 'TOC3', 'ILL' ]
                        }
                    },
                    'blank': {
                        'if': {
                            'field': 'tag4',
                            'is': 'EMPTY'
                        }
                    },
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

    def pp(self,val):
        printer = pprint.PrettyPrinter(indent=4)
        printer.pprint(val)

    def get_config(self):
        return settings.SPREADSHEET_CONFIG

    def test_init(self):
        sheet = OPWorkbook(self.helen_griffith_workbook, self.get_config()).pages
        self.assertIsInstance(sheet, PagesSheet)
        self.assertIsInstance(sheet, ValidatableSheet)

    def test_validate(self):
        sheet = OPWorkbook(self.pages_workbook, self.pages_config).pages
        sheet.validate()
        if len(sheet.errors) > 0: self.pp(sheet.errors)
        self.assertEqual(len(sheet.errors), 0)
