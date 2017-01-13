# -*- coding: utf-8 -*-

import json

PROJECTS = {
    'validations': {
        'unique_fields': [
            'tag',
            'name',
        ],
        'required_fields': [
            'tag',
            'live',
            'name',
            'blurb',
            'include_file',
            'csv_only',
        ],
    },
    'configs': [
        {
            'tag': 'bibliophilly',
            'name': 'Bibliotheca Philadelphiensis',
            'blurb': 'Lorem ipsum',
            'csv_only': False,
            'include_file': 'BiblioPhilly.html',
            'live': True,
        },
        {
            'tag': 'pacscl-diaries',
            'name': 'PACSCL Diares',
            'blurb': 'Lorem ipsum',
            'csv_only': False,
            'include_file': 'PACSCLDiaries.html',
            'live': True,
        },
        {
            'tag': 'thai',
            'name': 'Thai Manuscripts',
            'blurb': 'Lorem ipsum',
            'csv_only': True,
            'live': True,
        },
    ],
}

print json.dumps(PROJECTS)
