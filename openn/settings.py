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

DERIVS = {
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

COLLECTIONS = {
    'medren': {
        'tag': 'medren',
        'name': 'Penn Manuscripts',
        'blurb': 'These manuscripts are from the collections of the Rare Books and Manuscripts Library at the University of Pennsylvania or are hosted by Penn with the permission of their owners.  Penn holds over 2,000 Western manuscripts produced before the 19th century; medieval and Renaissance manuscripts comprise approximately 900 items, the earliest dating from 1000 A.D. The medieval manuscripts, now a collection of approximately 250 items, have been considered and used as a research collection since the private library of church historian Henry Charles Lea came to the University in the early 20th century. Most of the manuscripts are in Latin, but the medieval vernacular languages of Middle English, Middle French, Italian, Spanish, German, Dutch, and Judaeo-Arabic are each represented by one or more manuscripts. The collection is particularly strong in the fields of church history and history of science, with secondary strengths in liturgy and liturgical chant, theology and philosophy, and legal documents.',
        'toc_file': 'PennManuscripts.html',
        'include_file': 'PennManuscripts.html',
        'web_dir': 'Data/PennManuscripts',
        'html_dir': 'Data/PennManuscripts/html',
        'prep_class': 'openn.prep.medren_prep.MedrenPrep',
        'live': True,
        'package_validation': {
            'valid_names': ['*.tif', 'bibid.txt'],
            'invalid_names': ['CaptureOne', 'Output', '*[()]*'],
            'required_names': ['*.tif', 'bibid.txt'],
        },
        'config' : {
            'host': 'dla.library.upenn.edu',
            'path': '/dla/medren/pageturn.xml?id=MEDREN_{0}',
            'xsl': os.path.join(SITE_ROOT, 'xsl/pih2tei.xsl'),
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
    },
    'ljs': {
        'tag': 'ljs',
        'name': 'Lawrence J. Schoenberg Manuscripts',
        'live': True,
        'blurb': 'These manuscripts are from the Lawrence J. Schoenberg collection in the Rare Books and Manuscripts Library at the University of Pennsylvania.',
        'toc_file': 'LJSchoenbergManuscripts.html',
        'web_dir': 'Data/LJSchoenbergManuscripts',
        'html_dir': 'Data/LJSchoenbergManuscripts/html',
        'prep_class': 'openn.prep.medren_prep.MedrenPrep',
        'package_validation': {
            'valid_names': ['*.tif', 'bibid.txt'],
            'invalid_names': ['CaptureOne', 'Output', '*[()]*'],
            'required_names': ['*.tif', 'bibid.txt'],
        },
        'config' : {
            'host': 'dla.library.upenn.edu',
            'path': '/dla/medren/pageturn.xml?id=MEDREN_{0}',
            'xsl': os.path.join(SITE_ROOT, 'xsl/pih2tei.xsl'),
            'image_rights': {
                'Marked': 'False',
                'WebStatment': 'http://creativecommons.org/publicdomain/mark/1.0/',
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
    },
    'brynmawr' : {
        'tag': 'brynmawr',
        'name': 'Special Collections, Bryn Mawr College',
        'live': False,
        'blurb': 'Documents from Special Collections, Bryn Mawr College.',
        'toc_file': 'BrynMawrCollege.html',
        'web_dir': 'Data/BrynMawrCollege',
        'html_dir': 'Data/BrynMawrCollege/html',
        'prep_class': 'openn.prep.spreadsheet_prep.SpreadsheetPrep',
        'prep_class_kwargs': {
            'config_json': os.path.join(SITE_ROOT, 'pacscl_diaries.json')
        },
        'package_validation': {
            'valid_names': ['*.tif', '*.xlsx' ],
            'invalid_names': ['CaptureOne', 'Output', '*[()]*'],
            'required_names': ['*.tif', '*.xlsx'],
        },
        'config' : {
            'xsl': os.path.join(SITE_ROOT, 'xsl/spreadsheet_xml2tei.xsl'),
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
        },
    },
    'drexarc' : {
        'tag': 'drexarc',
        'name': 'Drexel University Archives',
        'live': False,
        'blurb': 'Documents from Drexel University Archives.',
        'toc_file': 'DrexelUniversity.html',
        'web_dir': 'Data/DrexelUniversity',
        'html_dir': 'Data/DrexelUniversity/html',
        'prep_class': 'openn.prep.spreadsheet_prep.SpreadsheetPrep',
        'prep_class_kwargs': {
            'config_json': os.path.join(SITE_ROOT, 'pacscl_diaries.json')
        },
        'package_validation': {
            'valid_names': ['*.tif', '*.xlsx' ],
            'invalid_names': ['CaptureOne', 'Output', '*[()]*'],
            'required_names': ['*.tif', '*.xlsx'],
        },
        'config' : {
            'xsl': os.path.join(SITE_ROOT, 'xsl/spreadsheet_xml2tei.xsl'),
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
        },
    },
    'drexmed' : {
        'tag': 'drexmed',
        'name': 'Legacy Center Archives & Special Collection, Drexel University College of Medicine.',
        'live': False,
        'blurb': 'Documents from the Legacy Center Archives & Special Collection, Drexel University College of Medicine.',
        'toc_file': 'DrexelMedicine.html',
        'web_dir': 'Data/DrexelMedicine',
        'html_dir': 'Data/DrexelMedicine/html',
        'prep_class': 'openn.prep.spreadsheet_prep.SpreadsheetPrep',
        'prep_class_kwargs': {
            'config_json': os.path.join(SITE_ROOT, 'pacscl_diaries.json')
        },
        'package_validation': {
            'valid_names': ['*.tif', '*.xlsx' ],
            'invalid_names': ['CaptureOne', 'Output', '*[()]*'],
            'required_names': ['*.tif', '*.xlsx'],
        },
        'config' : {
            'xsl': os.path.join(SITE_ROOT, 'xsl/spreadsheet_xml2tei.xsl'),
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
        },
    },
    'haverford' : {
        'tag': 'haverford',
        'name': 'Quaker and Special Collections, Haverford College',
        'live': False,
        'blurb': 'Documents from Quaker and Special Collections, Haverford College.',
        'toc_file': 'HaverfordCollege.html',
        'web_dir': 'Data/HaverfordCollege',
        'html_dir': 'Data/HaverfordCollege/html',
        'prep_class': 'openn.prep.spreadsheet_prep.SpreadsheetPrep',
        'prep_class_kwargs': {
            'config_json': os.path.join(SITE_ROOT, 'pacscl_diaries.json')
        },
        'package_validation': {
            'valid_names': ['*.tif', '*.xlsx' ],
            'invalid_names': ['CaptureOne', 'Output', '*[()]*'],
            'required_names': ['*.tif', '*.xlsx'],
        },
        'config' : {
            'xsl': os.path.join(SITE_ROOT, 'xsl/spreadsheet_xml2tei.xsl'),
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
        },
    },
    'lehigh' : {
        'tag': 'lehigh',
        'name': 'Special Collections, Lehigh University',
        'live': False,
        'blurb': 'Documents from Special Collections, Lehigh University.',
        'toc_file': 'SpecialCollectionsLehighUniversity.html',
        'web_dir': 'Data/SpecialCollectionsLehighUniversity',
        'html_dir': 'Data/HaverfordCollege/html',
        'prep_class': 'openn.prep.spreadsheet_prep.SpreadsheetPrep',
        'prep_class_kwargs': {
            'config_json': os.path.join(SITE_ROOT, 'pacscl_diaries.json')
        },
        'package_validation': {
            'valid_names': ['*.tif', '*.xlsx' ],
            'invalid_names': ['CaptureOne', 'Output', '*[()]*'],
            'required_names': ['*.tif', '*.xlsx'],
        },
        'config' : {
            'xsl': os.path.join(SITE_ROOT, 'xsl/spreadsheet_xml2tei.xsl'),
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
        },
    },
    'tlc' : {
        'tag': 'tlc',
        'name': 'The Library Company of Philadelphia',
        'live': False,
        'blurb': 'Documents from the Library Company of Philadelphia.',
        'toc_file': 'LibraryCompany.html',
        'web_dir': 'Data/LibraryCompany',
        'html_dir': 'Data/LibraryCompany/html',
        'prep_class': 'openn.prep.spreadsheet_prep.SpreadsheetPrep',
        'prep_class_kwargs': {
            'config_json': os.path.join(SITE_ROOT, 'pacscl_diaries.json')
        },
        'package_validation': {
            'valid_names': ['*.tif', '*.xlsx' ],
            'invalid_names': ['CaptureOne', 'Output', '*[()]*'],
            'required_names': ['*.tif', '*.xlsx'],
        },
        'config' : {
            'xsl': os.path.join(SITE_ROOT, 'xsl/spreadsheet_xml2tei.xsl'),
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
        },
    },
    'libpa' : {
        'tag': 'libpa',
        'name': 'Rare Collections Library, State Library of Pennsylvania',
        'live': False,
        'blurb': 'Documents from the Rare Collections Library, State Library of Pennsylvania.',
        'toc_file': 'StateLibraryOfPennsylvania.html',
        'web_dir': 'Data/StateLibraryOfPennsylvania',
        'html_dir': 'Data/StateLibraryOfPennsylvania/html',
        'prep_class': 'openn.prep.spreadsheet_prep.SpreadsheetPrep',
        'prep_class_kwargs': {
            'config_json': os.path.join(SITE_ROOT, 'pacscl_diaries.json')
        },
        'package_validation': {
            'valid_names': ['*.tif', '*.xlsx' ],
            'invalid_names': ['CaptureOne', 'Output', '*[()]*'],
            'required_names': ['*.tif', '*.xlsx'],
        },
        'config' : {
            'xsl': os.path.join(SITE_ROOT, 'xsl/spreadsheet_xml2tei.xsl'),
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
        },
    },
    'friendshl' : {
        'tag': 'friendshl',
        'name': 'Friends Historical Library, Swarthmare College',
        'live': False,
        'blurb': 'Documents from the Friends Historical Library, Swarthmare College.',
        'toc_file': 'FriendsHistoricalLibrary.html',
        'web_dir': 'Data/FriendsHistoricalLibrary',
        'html_dir': 'Data/FriendsHistoricalLibrary/html',
        'prep_class': 'openn.prep.spreadsheet_prep.SpreadsheetPrep',
        'prep_class_kwargs': {
            'config_json': os.path.join(SITE_ROOT, 'pacscl_diaries.json')
        },
        'package_validation': {
            'valid_names': ['*.tif', '*.xlsx' ],
            'invalid_names': ['CaptureOne', 'Output', '*[()]*'],
            'required_names': ['*.tif', '*.xlsx'],
        },
        'config' : {
            'xsl': os.path.join(SITE_ROOT, 'xsl/spreadsheet_xml2tei.xsl'),
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
        },
    },
    'hsp' : {
        'tag': 'hsp',
        'name': 'Historical Society of Pennsylvania',
        'live': False,
        'blurb': 'Documents from the Historical Society of Pennsylvania.',
        'toc_file': 'HistoricalSocietyOfPennsylvania.html',
        'web_dir': 'Data/HistoricalSocietyOfPennsylvania',
        'html_dir': 'Data/HistoricalSocietyOfPennsylvania/html',
        'prep_class': 'openn.prep.spreadsheet_prep.SpreadsheetPrep',
        'prep_class_kwargs': {
            'config_json': os.path.join(SITE_ROOT, 'pacscl_diaries.json')
        },
        'package_validation': {
            'valid_names': ['*.tif', '*.xlsx' ],
            'invalid_names': ['CaptureOne', 'Output', '*[()]*'],
            'required_names': ['*.tif', '*.xlsx'],
        },
        'config' : {
            'xsl': os.path.join(SITE_ROOT, 'xsl/spreadsheet_xml2tei.xsl'),
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
        },
    },
    'lts' : {
        'tag': 'lts',
        'name': 'Lutheran Theological Seminary',
        'live': False,
        'blurb': 'Documents from Lutheran Theological Seminary.',
        'toc_file': 'LutheranTheologicalSeminary.html',
        'web_dir': 'Data/LutheranTheologicalSeminary',
        'html_dir': 'Data/LutheranTheologicalSeminary/html',
        'prep_class': 'openn.prep.spreadsheet_prep.SpreadsheetPrep',
        'prep_class_kwargs': {
            'config_json': os.path.join(SITE_ROOT, 'pacscl_diaries.json')
        },
        'package_validation': {
            'valid_names': ['*.tif', '*.xlsx' ],
            'invalid_names': ['CaptureOne', 'Output', '*[()]*'],
            'required_names': ['*.tif', '*.xlsx'],
        },
        'config' : {
            'xsl': os.path.join(SITE_ROOT, 'xsl/spreadsheet_xml2tei.xsl'),
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
        },
    },
    'ulp' : {
        'tag': 'ulp',
        'name': 'Union League of Philadelphia',
        'live': False,
        'blurb': 'Documents from the Union League of Philadelphia.',
        'toc_file': 'UnionLeagueOfPhiladelphia.html',
        'web_dir': 'Data/UnionLeagueOfPhiladelphia',
        'html_dir': 'Data/UnionLeagueOfPhiladelphia/html',
        'prep_class': 'openn.prep.spreadsheet_prep.SpreadsheetPrep',
        'prep_class_kwargs': {
            'config_json': os.path.join(SITE_ROOT, 'pacscl_diaries.json')
        },
        'package_validation': {
            'valid_names': ['*.tif', '*.xlsx' ],
            'invalid_names': ['CaptureOne', 'Output', '*[()]*'],
            'required_names': ['*.tif', '*.xlsx'],
        },
        'config' : {
            'xsl': os.path.join(SITE_ROOT, 'xsl/spreadsheet_xml2tei.xsl'),
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
        },
    },
}

    # Kislak


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
