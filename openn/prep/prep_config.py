from copy import deepcopy
from openn.collections.collection import Collection
from openn.prep.prep_method import PrepMethod

class PrepConfig:
    def __init__(self, collection_config, prep_method_config):
        "docstring"
        self._collection  = Collection(collection_config)
        self._prep_method = PrepMethod(prep_method_config)

    def collection(self):
        return self._collection

    def prep_method(self):
        return self._prep_method
