from copy import deepcopy

from openn.openn_functions import *
from openn.prep.prep_config import PrepConfig
from openn.collections.configs import Configs

class PrepConfigFactory(object):
    def __init__(self, prep_configs_dict, prep_methods, collection_configs):
        """Create a new PrepConfigFactory with dict `prep_configs_dict`, and
list `prep_methods` and list of collection_configs.

        """
        self._prep_config_dict   = deepcopy(prep_configs_dict)
        self._prep_methods       = deepcopy(prep_methods)
        self._collection_configs = deepcopy(collection_configs)

    def get_collection_config(prep_configs_dict):
        """Extract the collection configuration from

        Arguments:
        - `prep_configs_dict`:
        """


    def create_prep_config(self, prep_config_dict):
        collection_t
        try:
            collection_tag  = prep_config_dict['collection']['tag']
        except KeyError:

            prep_method_tag = prep_config_dict['prep_method']['tag']
