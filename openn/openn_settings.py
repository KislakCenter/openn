# -*- coding: utf-8 -*-


import os
from copy import deepcopy
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "openn.settings")
from openn.openn_exception import OPennException
from django.conf import settings

class OPennSettings(object):
    def __init__(self,coll_name):
        """
        Create a new setttings object for the specified coll_name. An error is
        raised if the coll_name is not found.
        """
        self._coll_name = coll_name.lower()
        self._validate()

    @property
    def deriv_configs(self):
        """
        Returns settings.DERIVS. It looks like this:


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


        """
        return settings.DERIVS

    @property
    def coll(self):
        """
        Return the collection configuration. These are set up in
        the settings.COLLECTIONS dict. A collection is a dict like this:

            'medren': {
                'prep_class': 'openn.prep.medren_prep.MedrenPrep',
                'config' : {
                    'host': 'dla.library.upenn.edu',
                    'path': '/dla/medren/pageturn.xml?id=MEDREN_{0}',
                    'xsl': os.path.join(SITE_ROOT, 'xsl/pih2tei.xsl'),
                    'image_rights': {
                        'xmpRights:Marked': 'True',
                        'xmpRights:WebStatment': 'http://creativecommons.org/licenses/by-nc/4.0/',
                        'xmpRights:UsageTerms': ('This work and all referenced images are ©%d...' % today.year),
                        'dc:rights': ('This work and all referenced images are ©%d...' % today.year),
                        },
                    },
                },

        """
        return settings.COLLECTIONS[self._coll_name]

    @property
    def spreadsheet_config(self):
        return deepcopy(settings.SPREADSHEET_FIELDS)

    @property
    def known_colls(self):
        """ A list of all configured collections. """
        return settings.COLLECTIONS.keys()

    @property
    def coll_config(self):
        return self.coll.get('config', None)

    def deriv_config(self,deriv_type):
        """ Return the configuration for the given deriv_type. """
        return self.deriv_configs.get(deriv_type, None)

    def _validate(self):
        if not self._coll_name or not self._coll_name in settings.COLLECTIONS:
            msg = "No collection found for %s; expected one of %s"
            msg = msg % (self._coll_name, ','.join(self.known_colls))
            raise OPennException(msg)
