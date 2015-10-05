from copy import deepcopy
from openn.openn_exception import OPennException

from openn.models import *

class Collection:
    def __init__(self, collection_config):
        self._config = deepcopy(collection_config)
        self._openn_collection = None

    def openn_collection(self):
        if self._openn_collection is None:
            self._openn_collection = OPennCollection.objects.get(tag=self.tag())

        return self._openn_collection

    def config(self):
        return self._config

    def is_live(self):
        return self._config['live']

    def tag(self):
        return self._config['tag']

    def name(self):
        return self._config['name']

    def blurb(self):
        return self._config['blurb']

    def metadata_type(self):
        return self.openn_collection().metadata_type

    def long_id(self):
        return self.openn_collection().long_id()

    def folder(self):
        opcoll = self.openn_collection()
        if opcoll is not None:
            return opcoll.long_id()
        else:
            msg = "Collection with tag '%s' is not in db; has no folder"
            raise OPennException(msg % self.tag)

    def toc_file(self):
        return self.openn_collection().toc_file()

    def web_dir(self):
        return self.openn_collection().web_dir()

    def html_dir(self):
        return self.openn_collection().html_dir()

    def include_file(self):
        return self.config()['include_file']
