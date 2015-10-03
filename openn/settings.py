# -*- coding: utf-8 -*-

import os
import datetime

SECRET_KEY = None
skey_file = os.path.join(os.path.dirname(__file__), 'secret_key.txt')
today = datetime.date.today()
if os.environ.get('OPENN_SECRET_KEY') is not None:
    SECRET_KEY = os.environ['OPENN_SECRET_KEY']
elif os.path.exists(skey_file):
    SECRET_KEY = open(skey_file).read().strip()

REQUIRED_ENV_VARS = [
    'OPENN_DB_NAME',
    'OPENN_DB_USER',
    'OPENN_DB_PASSWORD',
    'OPENN_DB_HOST',
    'OPENN_SAXON_JAR',
    'OPENN_STAGING_DIR',
    'OPENN_PACKAGE_DIR' ]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ['OPENN_DB_NAME'],
        'USER': os.environ['OPENN_DB_USER'],
        'PASSWORD': os.environ['OPENN_DB_PASSWORD'],
        'HOST': os.environ['OPENN_DB_HOST'],
        'OPTIONS': {
            'init_command': 'SET storage_engine=INNODB,character_set_connection=utf8,collation_connection=utf8_unicode_ci',
        },
    }
}

# Files matching the following pattern will be cleaned from source
# directories.  The pattern must be a valid, UNCOMPILED python regular
# expression string.
CLOBBER_PATTERN = 'Thumbs.db|.*\.lnk'

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': os.environ['SDBM_DB_NAME'],
#         'USER': os.environ['SDBM_DB_USER'],
#         'PASSWORD': os.environ['SDBM_DB_PASSWORD'],
#         'HOST': os.environ['SDBM_DB_HOST'],
#         'OPTIONS': {
#             'init_command': 'SET storage_engine=INNODB',
#         },
#     }
# }

INSTALLED_APPS = (
        'openn', 'south', 'markdown_deux', 'ordered_model','django_extensions',
        )

SITE_ROOT = os.path.dirname(os.path.realpath(__file__))
PROJECT_PATH = os.path.abspath(os.path.dirname(__name__))

OPENN_HOST = 'openn.library.upenn.edu'

# put the openn/bin dir in the path
os.environ['PATH'] = os.path.join(PROJECT_PATH, 'bin') + os.pathsep + os.environ['PATH']

DERIV_CONFIGS = {
        'web': {
            'ext': 'jpg',
            'max_side': 1800,

            },
        'thumb': {
            'ext': 'jpg',
            'max_side': 190,
            },
        }

TEMPLATE_DIRS = (os.path.join(SITE_ROOT, 'templates'), )

README_TEMPLATES = [ { 'file': 'ReadMe.html', 'title': 'Read Me' },
                     { 'file': 'TechnicalReadMe.html', 'title': 'Technical Read Me' } ]
COLLECTIONS_TEMPLATE = 'Collections.html'

STAGING_DIR = os.environ['OPENN_STAGING_DIR']
PACKAGE_DIR = os.environ['OPENN_PACKAGE_DIR']
ARCHIVE_DIR = os.environ['OPENN_ARCHIVE_DIR']

TOC_DIR = 'html'

LICENCES = {
    'CC-BY': {
        'metadata': u'Metadata is ©{year} {holder} and licensed under a Creative Commons Attribution License version 4.0 (CC-BY-4.0 https://creativecommons.org/licenses/by/4.0/legalcode. For a description of the terms of use see the Creative Commons Deed https://creativecommons.org/licenses/by/4.0/. {more_information}',
        'image': u'Images are  ©{year} {holder} and licensed under a Creative Commons Attribution License version 4.0 (CC-BY-4.0 https://creativecommons.org/licenses/by/4.0/legalcode. For a description of the terms of use see the Creative Commons Deed https://creativecommons.org/licenses/by/4.0/. {more_information}',
        'single_image': u'This image of {title} is ©{year} {holder} and licensed under a Creative Commons Attribution License version 4.0 (CC-BY-4.0 https://creativecommons.org/licenses/by/4.0/legalcode. For a description of the terms of use see the Creative Commons Deed https://creativecommons.org/licenses/by/4.0/. {more_information}',

        'legalcode_url': 'https://creativecommons.org/licenses/by/4.0/legalcode',
        'deed_url': 'https://creativecommons.org/licenses/by/4.0/'
        },
    'CC0': {
        'metadata': u'To the extent possible under law, {holder} has waived all copyright and related or neighboring rights to this metadata about {title}. This work is published from: United States. For a summary of CC0, see https://creativecommons.org/publicdomain/zero/1.0/. Legal code: https://creativecommons.org/publicdomain/zero/1.0/legalcode.  {more_information}',
        'image': u'To the extent possible under law, {holder} has waived all copyright and related or neighboring rights to these images and the content of {title}. This work is published from: United States. For a summary of CC0, see https://creativecommons.org/publicdomain/zero/1.0/. Legal code: https://creativecommons.org/publicdomain/zero/1.0/legalcode. {more_information}',
        'single_image': u'To the extent possible under law, {holder} has waived all copyright and related or neighboring rights to this image and the content of {title}. This work is published from: United States. For a summary of CC0, see https://creativecommons.org/publicdomain/zero/1.0/. Legal code: https://creativecommons.org/publicdomain/zero/1.0/legalcode. {more_information}',
        'legalcode_url': 'https://creativecommons.org/publicdomain/zero/1.0/legalcode',
        'deed_url': 'https://creativecommons.org/publicdomain/zero/1.0/'
    },
    'PD': {
        'metadata': u'This metadata about {title} is free of known copyright restrictions and in the public domain. See the Creative Commons Public Domain Mark page for usage details, http://creativecommons.org/publicdomain/mark/1.0/. {more_information}',
        'image':  u'These images and the content of {title} are free of known copyright restrictions and in the public domain. See the Creative Commons Public Domain Mark page for usage details, http://creativecommons.org/publicdomain/mark/1.0/. {more_information}',
        'single_image':  u'This image and the content of {title} are free of known copyright restrictions and in the public domain. See the Creative Commons Public Domain Mark page for usage details, http://creativecommons.org/publicdomain/mark/1.0/. {more_information}',
        'legalcode_url': 'http://creativecommons.org/publicdomain/mark/1.0/',
        'deed_url': 'http://creativecommons.org/publicdomain/mark/1.0/'
    },
}

IMAGE_TYPES = ( '*.tif', '*.jpg' )


PREPARATION_METHODS = [
    {
        'tag': 'pih',
        'description': "Uses metadata scraped from Penn in Hand to build metadata for the object. Requires bibid.txt file containing the object's BibID",
        'name': 'Penn in Hand Prep',
        'package_validation': {
            'valid_names': ['*.tif', 'bibid.txt'],
            'invalid_names': ['CaptureOne', 'Output', '*[()]*'],
            'required_names': ['*.tif', 'bibid.txt'],
        },
        'prep_class': {
            'class_name': 'openn.prep.medren_prep.MedrenPrep',
            'params': {
                'pih_host': 'dla.library.upenn.edu',
                'pih_path': '/dla/medren/pageturn.xml?id=MEDREN_{0}',
                'xsl': os.path.join(SITE_ROOT, 'xsl/pih2tei.xsl'),
            },
        },
    },
    {
        'tag': 'diaries',
        'description': "Extracts metadata from PACSCL Diaries spreadsheet to build metadata for the object. Requires valid openn_metadata.xslx file.",
        'name': 'PACSCL Diaries Prep',
        'package_validation': {
            'valid_names': ['*.tif', '*.jpg', '*.xlsx'],
            'invalid_names': ['CaptureOne', 'Output', '*[()]*'],
            'required_names': ['*.xlsx'],
        },
        'prep_class': {
            'class_name': 'openn.prep.spreadsheet_prep.SpreadsheetPrep',
            'params' : {
                'image_rights': {
                    'dynamic': True,
                },
                'config_json': os.path.join(SITE_ROOT, 'pacscl_diaries.json'),
                'xsl': os.path.join(SITE_ROOT, 'xsl/spreadsheet_xml2tei.xsl'),
            },
        },
    }
]

COLLECTIONS = {
    'validations': {
        'unique_fields': [
            'tag',
            'name',
            'include_file',
        ],
        'required_fields': [
            'tag',
            'live',
            'name',
            'blurb',
            'include_file',
            'metadata_type',
        ],
    },
    'configs': [
        {
            'tag': 'pennmss',
            'metadata_type': 'TEI',
            'live': True,
            'name': 'Penn Manuscripts',
            'blurb': 'These manuscripts are from the collections of the Rare Books and Manuscripts Library at the University of Pennsylvania or are hosted by Penn with the permission of their owners.  Penn holds over 2,000 Western manuscripts produced before the 19th century; medieval and Renaissance manuscripts comprise approximately 900 items, the earliest dating from 1000 A.D. The medieval manuscripts, now a collection of approximately 250 items, have been considered and used as a research collection since the private library of church historian Henry Charles Lea came to the University in the early 20th century. Most of the manuscripts are in Latin, but the medieval vernacular languages of Middle English, Middle French, Italian, Spanish, German, Dutch, and Judaeo-Arabic are each represented by one or more manuscripts. The collection is particularly strong in the fields of church history and history of science, with secondary strengths in liturgy and liturgical chant, theology and philosophy, and legal documents.',
            'include_file': 'PennManuscripts.html',
        },
        {
            'tag': 'ljs',
            'metadata_type': 'TEI',
            'live': True,
            'name': 'Lawrence J. Schoenberg Manuscripts',
            'blurb': 'These manuscripts are from the Lawrence J. Schoenberg collection in the Rare Books and Manuscripts Library at the University of Pennsylvania.',
            'include_file': 'LJSchoenbergManuscripts.html',
        },
        {
            'tag': 'brynmawr',
            'metadata_type': 'TEI',
            'live': False,
            'name': 'Special Collections, Bryn Mawr College',
            'blurb': 'Documents from Special Collections, Bryn Mawr College.',
            'include_file': 'BrynMawrCollege.html',
        },
        {
            'tag': 'drexarc',
            'name': 'Drexel University Archives',
            'metadata_type': 'TEI',
            'live': False,
            'blurb': 'Documents from Drexel University Archives.',
            'include_file': 'DrexelUniversity.html',
        },
        {
            'tag': 'drexmed',
            'name': 'Legacy Center Archives & Special Collection, Drexel University College of Medicine.',
            'metadata_type': 'TEI',
            'live': False,
            'blurb': 'Documents from the Legacy Center Archives & Special Collection, Drexel University College of Medicine.',
            'include_file': 'DrexelMedicine.html',
        },
        {
            'tag': 'haverford',
            'name': 'Quaker and Special Collections, Haverford College',
            'metadata_type': 'TEI',
            'live': False,
            'blurb': 'Documents from Quaker and Special Collections, Haverford College.',
            'include_file': 'HaverfordCollege.html',
        },
        {
            'tag': 'lehigh',
            'name': 'Special Collections, Lehigh University',
            'metadata_type': 'TEI',
            'live': False,
            'blurb': 'Documents from Special Collections, Lehigh University.',
            'include_file': 'SpecialCollectionsLehighUniversity.html',
        },
        {
            'tag': 'tlc',
            'name': 'The Library Company of Philadelphia',
            'metadata_type': 'TEI',
            'live': False,
            'blurb': 'Documents from the Library Company of Philadelphia.',
            'include_file': 'LibraryCompany.html',
        },
        {
            'tag': 'libpa',
            'name': 'Rare Collections Library, State Library of Pennsylvania',
            'metadata_type': 'TEI',
            'live': False,
            'blurb': 'Documents from the Rare Collections Library, State Library of Pennsylvania.',
            'include_file': 'StateLibraryOfPennsylvania.html',
        },
        {
            'tag': 'friendshl',
            'name': 'Friends Historical Library, Swarthmare College',
            'metadata_type': 'TEI',
            'live': False,
            'blurb': 'Documents from the Friends Historical Library, Swarthmare College.',
            'include_file': 'FriendsHistoricalLibrary.html',
        },
        {
            'tag': 'hsp',
            'name': 'Historical Society of Pennsylvania',
            'metadata_type': 'TEI',
            'live': False,
            'blurb': 'Documents from the Historical Society of Pennsylvania.',
            'include_file': 'HistoricalSocietyOfPennsylvania.html',
        },
        {
            'tag': 'lts',
            'name': 'Lutheran Theological Seminary',
            'metadata_type': 'TEI',
            'live': False,
            'blurb': 'Documents from Lutheran Theological Seminary.',
            'include_file': 'LutheranTheologicalSeminary.html',
        },
        {
            'tag': 'ulp',
            'name': 'Union League of Philadelphia',
            'metadata_type': 'TEI',
            'live': False,
            'blurb': 'Documents from the Union League of Philadelphia.',
            'include_file': 'UnionLeagueOfPhiladelphia.html',
        },
    ],
}

PREP_CONFIGS = {
    'penn-pih': {
        'collection': {
            'tag': 'pennmss',
        },
        "image_types": [ '*.tif' ],
        'collection_prep': {
            'tag': 'pih',
        },
        'common_prep': {
            'image_rights': {
                'Marked': 'False',
                'WebStatement': 'http://creativecommons.org/publicdomain/mark/1.0/',
                'UsageTerms': 'This image and its content are free of known copyright restrictions and in the public domain. See the Creative Commons Public Domain Mark page for usage details, http://creativecommons.org/publicdomain/mark/1.0/.',
                'rights': 'This image and its content are free of known copyright restrictions and in the public domain. See the Creative Commons Public Domain Mark page for usage details, http://creativecommons.org/publicdomain/mark/1.0/.',
            },
            'rights_statements': {
                'images': {
                    'url': 'http://creativecommons.org/publicdomain/mark/1.0/',
                    'text': 'Unless otherwise stated, all images and their content are free of known copyright restrictions and in the public domain. See the Creative Commons Public Domain Mark page for more information on terms of use, <a href="http://creativecommons.org/publicdomain/mark/1.0/">http://creativecommons.org/publicdomain/mark/1.0/</a>',
                },
                'metadata': {
                    'url': 'http://creativecommons.org/licenses/by/4.0/',
                    'text': ('Unless otherwise stated, all manuscript descriptions and other cataloging metadata are ©%d The University of Pennsylvania Libraries. They are licensed for use under a Creative Commons Attribution License version 4.0 (CC-BY-4.0 <a href="https://creativecommons.org/licenses/by/4.0/legalcode">https://creativecommons.org/licenses/by/4.0/legalcode</a>. For a description of the terms of use see the Creative Commons Deed <a href="https://creativecommons.org/licenses/by/4.0/">https://creativecommons.org/licenses/by/4.0/</a>' % (today.year, )),
                },
            },
        }
    },
    'ljs-pih': {
        'collection': {
            'tag': 'ljs'
        },
        "image_types": [ '*.tif' ],
        'collection_prep': {
            'tag': 'pih',
            }
        },
        'common_prep': {
            'image_rights': {
                'Marked': 'False',
                'WebStatement': 'http://creativecommons.org/publicdomain/mark/1.0/',
                'UsageTerms': 'This image and its content are free of known copyright restrictions and in the public domain. See the Creative Commons Public Domain Mark page for usage details, http://creativecommons.org/publicdomain/mark/1.0/.',
                'rights': 'This image and its content are free of known copyright restrictions and in the public domain. See the Creative Commons Public Domain Mark page for usage details, http://creativecommons.org/publicdomain/mark/1.0/.',
            },
            'rights_statements': {
                'images': {
                    'url': 'http://creativecommons.org/publicdomain/mark/1.0/',
                    'text': 'Unless otherwise stated, all images and their content are free of known copyright restrictions and in the public domain. See the Creative Commons Public Domain Mark page for more information on terms of use, <a href="http://creativecommons.org/publicdomain/mark/1.0/">http://creativecommons.org/publicdomain/mark/1.0/</a>',
                },
                'metadata': {
                    'url': 'http://creativecommons.org/licenses/by/4.0/',
                    'text': ('Unless otherwise stated, all manuscript descriptions and other cataloging metadata are ©%d The University of Pennsylvania Libraries. They are licensed for use under a Creative Commons Attribution License version 4.0 (CC-BY-4.0 <a href="https://creativecommons.org/licenses/by/4.0/legalcode">https://creativecommons.org/licenses/by/4.0/legalcode</a>. For a description of the terms of use see the Creative Commons Deed <a href="https://creativecommons.org/licenses/by/4.0/">https://creativecommons.org/licenses/by/4.0/</a>' % (today.year, )),
                },
            },

    },
    'brynmawr-diaries': {
        'collection': {
            'tag': 'brynmawr'
        },
        "image_types": [ '*.tif' ],
        'collection_prep': {
            'tag': 'diaries',
        },
        'common_prep': {
            'image_rights': {
                'dynamic': True,
            },
            'rights_statements': {
                'images': {
                    'dynamic': True,
                },
                'metadata': {
                    'dynamic': True,
                },
            },
        }
    },
    'haverford-diaries': {
        'collection': {
            'tag': 'haverford'
        },
        "image_types": [ '*.tif' ],
        'collection_prep': {
            'tag': 'diaries',
        },
        'common_prep': {
            'image_rights': {
                'dynamic': True,
            },
            'rights_statements': {
                'images': {
                    'dynamic': True,
                },
                'metadata': {
                    'dynamic': True,
                },
            },
        }
    }
}

PREP_CONTEXT = {
    'archive_dir': ARCHIVE_DIR,
    'package_dir': PACKAGE_DIR,
    'staging_dir': STAGING_DIR,
    'licences': LICENCES,
    'deriv_configs': DERIV_CONFIGS,
}

MARKDOWN_DEUX_STYLES = {
    "default": {
        "extras": {
            "code-friendly": None,
            'fenced-code-blocks': None,
            'toc': None,
        },
        "safe_mode": "escape",
    },
    "trusted": {
        "extras": {
            "code-friendly": None,
        },
        "safe_mode": False,
    }
}
