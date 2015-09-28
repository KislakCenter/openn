from copy import deepcopy

class Collection:
    def __init__(self, collection_config):
        self._config = deepcopy(collection_config)
