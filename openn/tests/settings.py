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

DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
            'NAME': 'openn/tests/database.sqlite3',                      # Or path to database file if using sqlite3.
            }
        }

INSTALLED_APPS = (
        'openn', 'south', 'ordered_model',
        )

SITE_ROOT = os.path.dirname(os.path.realpath(__file__))
PROJECT_PATH = os.path.abspath(os.path.dirname(__name__))

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

TEMPLATE_DIRS = ('openn/templates', )

STAGING_DIR = 'openn/tests/staging/site'

COLLECTIONS = {
        'medren': {
            'tag': 'medren',
            'name': 'Penn Manuscripts',
            'blurb': 'This manuscripts are from the collections of the Rare Books and Manuscripts Library at the University of Pennsylvania or are hosted by Penn with permission of their owners.',
            'toc_file': 'TOC_PennManuscripts.html',
            'web_dir': 'Data/PennManuscripts',
            'html_dir': 'Date/PennManuscripts/html',
            'prep_class': 'openn.prep.medren_prep.MedrenPrep',
            'config' : {
                'host': 'dla.library.upenn.edu',
                'path': '/dla/medren/pageturn.xml?id=MEDREN_{0}',
                'xsl': os.path.join(PROJECT_PATH, 'openn/xsl/pih2tei.xsl'),
                'image_rights': {
                    'Marked': 'True',
                    'WebStatment': 'http://creativecommons.org/licenses/by-nc/4.0/',
                    'UsageTerms': ('This work and all referenced images are ©%d University of Pennsylvania. They are licensed under a Creative Commons Attribution-NonCommercial 4.0 International License (CC BY-NC 4.0), http://creativecommons.org/licenses/by-nc/4.0/.' % today.year),
                    'rights': ('This work and all referenced images are ©%d University of Pennsylvania. They are licensed under a Creative Commons Attribution-NonCommercial 4.0 International License (CC BY-NC 4.0), http://creativecommons.org/licenses/by-nc/4.0/.' % today.year),
                    },
                },
            },

            'ljs': {
                'tag': 'ljs',
                'name': 'Lawrence J. Schoenberg Manuscripts',
                'blurb': 'This manuscripts are from the Lawrence J. Schoenberg collection in the Rare Books and Manuscripts Library at the University of Pennsylvania.',
                'toc_file': 'TOC_LJSchoenberg_Manuscripts.html',
                'web_dir': 'Data/LJSchoenberg_Manuscripts',
                'html_dir': 'Date/LJSchoenberg_Manuscripts/html',
                'prep_class': 'openn.prep.medren_prep.MedrenPrep',
                'config' : {
                    'host': 'dla.library.upenn.edu',
                    'path': '/dla/medren/pageturn.xml?id=MEDREN_{0}',
                    'xsl': os.path.join(PROJECT_PATH, 'openn/xsl/pih2tei.xsl'),
                    'image_rights': {
                        'Marked': 'True',
                        'WebStatment': 'http://creativecommons.org/licenses/by-nc/4.0/',
                        'UsageTerms': ('This work and all referenced images are ©%d University of Pennsylvania. They are licensed under a Creative Commons Attribution-NonCommercial 4.0 International License (CC BY-NC 4.0), http://creativecommons.org/licenses/by-nc/4.0/.' % today.year),
                        'rights': ('This work and all referenced images are ©%d University of Pennsylvania. They are licensed under a Creative Commons Attribution-NonCommercial 4.0 International License (CC BY-NC 4.0), http://creativecommons.org/licenses/by-nc/4.0/.' % today.year),
                    },
                },
            },

        }
