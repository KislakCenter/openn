from copy import deepcopy
from openn.openn_exception import OPennException

from openn.models import *

class Collection:
    def __init__(self, collection_config):
        self._config = deepcopy(collection_config)

    def openn_collection(self):
        try:
            return OPennCollection.objects.get(tag=self.tag())
        except OPennCollection.DoesNotExist:
            return None

    def tag(self):
        return self._config['tag']

    def folder(self):
        opcoll = self.openn_collection()
        if opcoll is not None:
            return opcoll.long_id()
        else:
            msg = "Collection with tag '%s' is not in db; has no folder"
            raise OPennException(msg % self.tag)
