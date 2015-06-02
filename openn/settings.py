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

TOC_DIR = 'html'


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
    'ljs': {
        'tag': 'ljs',
        'name': 'Lawrence J. Schoenberg Manuscripts',
        'blurb': 'These manuscripts are from the Lawrence J. Schoenberg collection in the Rare Books and Manuscripts Library at the University of Pennsylvania.',
        'toc_file': 'TOC_LJSchoenbergManuscripts.html',
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
    'bryn_mawr' : {
        'tag': 'brynmawr',
        'name': 'BrynMawrCollege',
        'blurb': 'Diaries from the Bryn Mawr College Special Collections.',
        'toc_file': 'TOC_BrynMawrCollege.html',
        'web_dir': 'Data/BrynMawrCollege',
        'html_dir': 'Data/BrynMawrCollege/html',
        'prep_class': 'openn.prep.medren_prep.SpreadsheetPrep',
        'package_validation': {
            'valid_names': ['*.tif', '*.xlsx' ],
            'invalid_names': ['CaptureOne', 'Output', '*[()]*'],
            'required_names': ['*.tif', '*.xlsx'],
        },
        'config' : {
            'image_rights': {
                'dynamic': 'True',
            },
            'rights_statements': {
                'images': {
                    'dynamic': 'True',
                },
                'metadata': {
                    'dynamic': 'True',
                },
            },
        },
    },
    'haverford' : {
        'tag': 'haverford',
        'name': 'HaverfordCollege',
        'blurb': 'Documents from Haverford College Special Collections.',
        'toc_file': 'TOC_HaverfordCollege.html',
        'web_dir': 'Data/HaverfordCollege',
        'html_dir': 'Data/HaverfordCollege/html',
        'prep_class': 'openn.prep.medren_prep.SpreadsheetPrep',
        'package_validation': {
            'valid_names': ['*.tif', '*.xlsx' ],
            'invalid_names': ['CaptureOne', 'Output', '*[()]*'],
            'required_names': ['*.tif', '*.xlsx'],
        },
        'config' : {
            'image_rights': {
                'dynamic': 'True',
            },
            'rights_statements': {
                'images': {
                    'dynamic': 'True',
                },
                'metadata': {
                    'dynamic': 'True',
                },
            },
        },
    },

}

SPREADSHEET_CONFIG = {
    'description': {
        'sheet_name': 'Description',
        'data_offset': 2,
        'heading_type': 'row', # headings on left, data read left-to-right
        'fields': {
            'administrative_contact': {
                'field_name': 'Administrative Contact',
                'required': True,
                'repeating': True,
                'data_type': 'string'
            },
            'administrative_contact_email': {
                'field_name': 'Administrative Contact email',
                'required': True,
                'repeating': True,
                'data_type': 'email'
            },
            'pacscl_diaries_project_id': {
                'field_name': 'PACSCL Diaries Project ID',
                'required': False,
                'repeating': False,
                'data_type': 'string'
            },
            'metadata_creator': {
                'field_name': 'Metadata Creator',
                'required': True,
                'repeating': True,
                'data_type': 'string'
            },
            'metadata_creator_email': {
                'field_name': 'Metadata Creator Email',
                'required': True,
                'repeating': True,
                'data_type': 'email'
            },
            'repository_city': {
                'field_name': 'Repository City',
                'required': True,
                'repeating': False,
                'data_type': 'string'
            },
            'repository_name': {
                'field_name': 'Repository Name',
                'required': True,
                'repeating': False,
                'data_type': 'string'
            },
            'source_collection': {
                'field_name': 'Source collection',
                'required': False,
                'repeating': True,
                'data_type': 'string'
            },
            'call_numberid': {
                'field_name': 'Call Number/ID',
                'required': True,
                'repeating': True,
                'data_type': 'string'
            },
            'alternate_id': {
                'field_name': 'Alternate ID',
                'required': False,
                'repeating': False,
                'data_type': 'string'
            },
            'alternate_id_type': {
                'field_name': 'Alternate ID type',
                'required':  {
                    'if': {
                        'field': 'alternate_id',
                        'is': 'NONEMPTY',
                    }
                },
                'blank': {
                    'if': {
                        'field': 'alternate_id',
                        'is': 'EMPTY'
                    }
                },
                'repeating': False,
                'data_type': 'string'
            },
            'title': {
                'field_name': 'Title',
                'required': True,
                'repeating': True,
                'data_type': 'string'
            },
            'volume_number': {
                'field_name': 'Volume number',
                'required': False,
                'repeating': False,
                'data_type': 'string'
            },
            'creator_name': {
                'field_name': 'Creator name',
                'required': True,
                'repeating': True,
                'data_type': 'string'
            },
            'creator_uri': {
                'field_name': 'Creator URI',
                'required': False,
                'repeating': True,
                'data_type': 'uri'
            },
            'date_single': {
                'field_name': 'Date (single)',
                'required': {
                    'if': {
                        'field': 'date_range_start',
                        'is': 'EMPTY'
                    }
                },
                'blank': {
                    'if': {
                        'field': 'date_range_start',
                        'is': 'NONEMPTY'
                    }
                },
                'repeating': False,
                'data_type': 'year',
            },
            'date_range_start': {
                'field_name': 'Date (range) start',
                'required': {
                    'if': {
                        'field': 'date_single',
                        'is': 'EMPTY'
                    }
                },
                'blank': {
                    'if': {
                        'field': 'date_single',
                        'is': 'NONEMPTY'
                    }
                },
                'repeating': False,
                'data_type': 'year'
            },
            'date_range_end': {
                'field_name': 'Date (range) end',
                'required': {
                    'if': {
                        'field': 'date_range_start',
                        'is': 'NONEMPTY'
                    }
                },
                'blank': {
                    'if': {
                        'field': 'date_range_start',
                        'is': 'EMPTY'
                    }
                },
                'repeating': False,
                'data_type': 'year'
            },
            'date_narrative': {
                'field_name': 'Date (narrative)',
                'required': False,
                'repeating': True,
                'data_type': 'string'
            },
            'place_of_origin': {
                'field_name': 'Place of origin',
                'required': True,
                'repeating': True,
                'data_type': 'string'
            },
            'description': {
                'field_name': 'Description',
                'required': False,
                'repeating': True,
                'data_type': 'string'
            },
            'language': {
                'field_name': 'Language',
                'required': True,
                'repeating': True,
                'data_type': 'lang'
            },
            'page_count': {
                'field_name': 'Number of physical pages',
                'required': False,
                'repeating': True,
                'data_type': 'string'
            },
            'page_gaps_in_images': {
                'field_name': 'Gaps',
                'required': False,
                'repeating': True,
                'data_type': 'string'
            },
            'page_dimensions': {
                'field_name': 'Page dimensions',
                'required': False,
                'repeating': True,
                'data_type': 'string'
            },
            'bound_dimensions': {
                'field_name': 'Bound dimensions',
                'required': False,
                'repeating': True,
                'data_type': 'string'
            },
            'related_resource': {
                'field_name': 'Related resource',
                'required': False,
                'repeating': True,
                'data_type': 'string'
            },
            'related_resource_url': {
                'field_name': 'Related resource URL',
                'required': False,
                'repeating': True,
                'data_type': 'uri'
            },
            'subject_names': {
                'field_name': 'Subject: names',
                'required': False,
                'repeating': True,
                'data_type': 'string'
            },
            'subject_names_uri': {
                'field_name': 'Subject: names URI [?]',
                'required': False,
                'repeating': True,
                'data_type': 'uri'
            },
            'subject_topical': {
                'field_name': 'Subject: topical',
                'required': False,
                'repeating': True,
                'data_type': 'string'
            },
            'subject_topical_uri': {
                'field_name': 'Subject: topical URI [?]',
                'required': False,
                'repeating': True,
                'data_type': 'uri'
            },
            'subject_geographic': {
                'field_name': 'Subject: geographic',
                'required': True,
                'repeating': False,
                'data_type': 'string'
            },
            'subject_geographic_uri': {
                'field_name': 'Subject: geographic URI [?]',
                'required': True,
                'repeating': False,
                'data_type': 'uri'
            },
            'subject_genreform': {
                'field_name': 'Subject: genre/form',
                'required': True,
                'repeating': False,
                'data_type': 'string'
            },
            'subject_genreform_uri': {
                'field_name': 'Subject: genre/form URI [?]',
                'required': True,
                'repeating': False,
                'data_type': 'uri'
            },
            'image_rights': {
                'field_name': 'Image rights',
                'required': True,
                'repeating': False,
                'data_type': 'string',
                'value_list': [ 'CC-BY', 'CC0', 'PD' ]
            },
            'image_copyright_holder': {
                'field_name': 'Image copyright holder',
                'required': {
                    'if': {
                        'field': 'image_rights',
                        'is': [ 'CC-BY', 'CC0' ]
                    }
                },
                'blank': {
                    'if': {
                        'field': 'image_rights',
                        'is': [ 'PD' ]
                    }
                },
                'repeating': False,
                'data_type': 'string'
            },
            'image_copyright_year': {
                'field_name': 'Image copyright year',
                'required': {
                    'if': {
                        'field': 'image_rights',
                        'is': [ 'CC-BY', 'CC0' ]
                    }
                },
                'blank': {
                    'if': {
                        'field': 'image_rights',
                        'is': [ 'PD' ]
                    }
                },
                'repeating': False,
                'data_type': 'year'
            },
            'metadata_rights': {
                'field_name': 'Metadata rights',
                'required': True,
                'repeating': False,
                'data_type': 'string',
                'value_list': [ 'CC-BY', 'CC0', 'PD' ]
            },
            'metadata_copyright_holder': {
                'field_name': 'Metadata copyright holder',
                'required':  {
                    'if': {
                        'field': 'metadata_rights',
                        'is': [ 'CC-BY', 'CC0' ]
                    }
                },
                'blank': {
                    'if': {
                        'field': 'metadata_rights',
                        'is': [ 'PD' ]
                    }
                },
                'repeating': False,
                'data_type': 'string'
            },
            'metadata_copyright_year': {
                'field_name': 'Metadata copyright year',
                'required':  {
                    'if': {
                        'field': 'metadata_rights',
                        'is': [ 'CC-BY', 'CC0' ]
                    }
                },
                'blank': {
                    'if': {
                        'field': 'metadata_rights',
                        'is': [ 'PD' ]
                    }
                },
                'repeating': False,
                'data_type': 'year'
            }
        }
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
                 'data_type': 'string'
            },
            'file_name': {
                'field_name': 'FILE_NAME',
                'required': {
                    'if': {
                        'field': 'display_page',
                        'is': 'NONEMPTY'
                    }
                 },
                 'repeating': True,
                'data_type': 'string'
            },
            'tag1': {
                'field_name': 'TAG1',
                'required': False,
                'repeating': True,
                'data_type': 'string'
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
                'data_type': 'string'
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
                'data_type': 'string'
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
                'data_type': 'string'
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
