from copy import deepcopy
import json

from openn.prep.prep_config import PrepConfig
from openn.prep.prep_methods import PrepMethods
from openn.collections.configs import Configs
from openn.openn_exception import OPennException

class PrepConfigFactory(object):
    def __init__(self, prep_configs_dict, prep_methods, collection_configs,
                 prep_context):
        """Create a new PrepConfigFactory with dict `prep_configs_dict`, and
list `prep_methods` and list of collection_configs.

        """
        self._prep_configs       = deepcopy(prep_configs_dict)
        self._prep_methods       = PrepMethods(prep_methods)
        self._collection_configs = Configs(collection_configs)
        self._prep_context       = deepcopy(prep_context)

    def create_prep_config(self, prep_config_tag):
        """For the given PREP_CONFIG tag `tag`, return a PrepConfig.
        """
        prep_config_dict = self._get_prep_config_dict(prep_config_tag)
        coll_config = self._get_coll_config_dict(prep_config_tag)
        method_config = self._get_prep_method_dict(prep_config_tag)
        return PrepConfig(**{
            'prep_config_tag': prep_config_tag,
            'coll_prep_dict': prep_config_dict,
            'coll_dict': coll_config,
            'prep_dict': method_config,
            'prep_context': self._prep_context,
        })

    def prep_config_tags(self):
        return sorted(self._prep_configs.keys())

    def _get_prep_config_dict(self, tag):
        try:
            return self._prep_configs[tag]
        except KeyError:
            msg = "Could not find prep_config_dict for tag '%s' (known: %s)"
            msg = msg % (tag,self.prep_config_tags())
            raise OPennException(msg)

    def _get_coll_config_dict(self, prep_config_tag):
        prep_config_dict = self._get_prep_config_dict(prep_config_tag)
        coll_tag = None
        try:
            coll_tag = prep_config_dict['collection']['tag']
        except KeyError:
            msg = "Could not find collection tag in dict: %r"
            msg = msg % (prep_config_dict,)
            raise OPennException(msg)

        return self._collection_configs.get_config(coll_tag)

    def _get_prep_method_dict(self, prep_config_tag):
        prep_config_dict = self._get_prep_config_dict(prep_config_tag)
        method_tag = None
        try:
            method_tag = prep_config_dict['collection_prep']['tag']
        except KeyError:
            msg = "Could not find ['collection_prep']['tag'] in dict: %r"
            msg = msg % (prep_config_dict,)
            raise OPennException(msg)

        return self._prep_methods.get_method_config(method_tag)
