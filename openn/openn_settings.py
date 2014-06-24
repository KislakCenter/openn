import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "openn.settings")
from openn.openn_exception import OPennException
from django.conf import settings

class OPennSettings(object):
    def __init__(self,coll_name):
        self.coll_name = coll_name.lower() if coll_name else None

    @property
    def settings(self):
        return settings

    @property
    def deriv_configs(self):
        return settings.DERIVS

    @property
    def coll(self):
        if not self.coll_name or not self.coll_name in settings.COLLECTIONS:
            msg = "No collection found for %s; expected one of %s" 
            msg = msg % (self.coll_name, ','.join(self.known_colls))
            raise OPennException(msg)
        return settings.COLLECTIONS[self.coll_name]

    @property
    def known_colls(self):
        return settings.COLLECTIONS.keys()

    @property
    def coll_config(self):
        return self.coll.get('config', None)

    def deriv_config(self,deriv_type):
        return self.deriv_configs.get(deriv_type, None)

