from copy import deepcopy

class PrepConfig:
    def __init__(self, collection_config, prep_method_config):
        "docstring"
        self._collection_config  = deepcopy(collection_config)
        self._prep_method_config = deepcopy(prep_method_config)
