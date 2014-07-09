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
            'NAME': 'openn/database.sqlite3',                      # Or path to database file if using sqlite3.
            }
        }

INSTALLED_APPS = (
        'openn', 'south',
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

COLLECTIONS = {
        'medren': {
            'prep_class': 'openn.prep.medren_prep.MedrenPrep',
            'config' : {
                'host': 'dla.library.upenn.edu',
                'path': '/dla/medren/pageturn.xml?id=MEDREN_{0}',
                'xsl': os.path.join(SITE_ROOT, 'xsl/pih2tei.xsl'),
                'image_rights': {
                    'Marked': 'True',
                    'WebStatment': 'http://creativecommons.org/licenses/by-nc/4.0/',
                    'UsageTerms': ('This work and all referenced images are ©%d University of Pennsylvania. They are licensed under a Creative Commons Attribution-NonCommercial 4.0 International License (CC BY-NC 4.0), http://creativecommons.org/licenses/by-nc/4.0/.' % today.year),
                    'rights': ('This work and all referenced images are ©%d University of Pennsylvania. They are licensed under a Creative Commons Attribution-NonCommercial 4.0 International License (CC BY-NC 4.0), http://creativecommons.org/licenses/by-nc/4.0/.' % today.year),
                    },
                },
            },
        }
