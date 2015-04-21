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

README_TEMPLATES = [ '0_ReadMe.html', '1_TechnicalReadMe.html' ]
COLLECTIONS_TEMPLATE = '3_Collections.html'

STAGING_DIR = os.environ['OPENN_STAGING_DIR']
PACKAGE_DIR = os.environ['OPENN_PACKAGE_DIR']

TOC_DIR = 'Collections'


COLLECTIONS = {
    'medren': {
        'tag': 'medren',
        'name': 'Penn Manuscripts',
        'blurb': 'These manuscripts are from the collections of the Rare Books and Manuscripts Library at the University of Pennsylvania or are hosted by Penn with the permission of their owners.',
        'toc_file': 'TOC_PennManuscripts.html',
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
                'include_file': 'LJSchoenbergManuscripts.html',
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
}
