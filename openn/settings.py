import os

SECRET_KEY = None
skey_file = os.path.join(os.path.dirname(__file__), 'secret_key.txt')
if os.environ.get('OPENN_SECRET_KEY') is not None:
    SECRET_KEY = os.environ['OPENN_SECRET_KEY']
elif os.path.exists(skey_file):
    SECRET_KEY = open(skey_file).read().strip()

DATABASES = { 
        'default': {
            'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
            'NAME': 'openn/database.sqlite3',                      # Or path to database file if using sqlite3.
            'USER': '',                      # Not used with sqlite3.
            'PASSWORD': '',                  # Not used with sqlite3.
            'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
            'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
            }   
        }

INSTALLED_APPS = ( 
        'openn', 'south',
        )   

COLLECTIONS = {
        'medren': {
            'prep_class': 'openn.prep.medren_prep.MedrenPrep',
            'kwargs' : { 
                'host': 'dla.library.upenn.edu', 
                'path': '/dla/medren/pageturn.xml?id=MEDREN_{0}',
                },
            },
        }
