from copy import deepcopy
import json

from openn.prep.prep_config import PrepConfig
from openn.prep.prep_methods import PrepMethods
from openn.repository.configs import Configs
from openn.openn_exception import OPennException

class PrepConfigFactory(object):
    def __init__(self, prep_configs_dict, prep_methods, repository_configs,
                 prep_context):
        """Create a new PrepConfigFactory with dict `prep_configs_dict`, and
list `prep_methods` and list of repository_configs.

        """
        self._prep_configs       = deepcopy(prep_configs_dict)
        self._prep_methods       = PrepMethods(prep_methods)
        self._repository_configs = Configs(repository_configs)
        self._prep_context       = deepcopy(prep_context)

    def create_prep_config(self, prep_config_tag):
        """For the given PREP_CONFIG tag `tag`, return a PrepConfig.
        """
        prep_config_dict = self._get_prep_config_dict(prep_config_tag)
        repo_config = self._get_repo_config_dict(prep_config_tag)
        method_config = self._get_prep_method_dict(prep_config_tag)
        return PrepConfig(**{
            'prep_config_tag': prep_config_tag,
            'repo_prep_dict': prep_config_dict,
            'repo_dict': repo_config,
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

    def _get_repo_config_dict(self, prep_config_tag):
        prep_config_dict = self._get_prep_config_dict(prep_config_tag)
        repo_tag = None
        try:
            repo_tag = prep_config_dict['repository']['tag']
        except KeyError:
            msg = "Could not find repository tag in dict: %r"
            msg = msg % (prep_config_dict,)
            raise OPennException(msg)

        return self._repository_configs.get_config(repo_tag)

    def _get_prep_method_dict(self, prep_config_tag):
        prep_config_dict = self._get_prep_config_dict(prep_config_tag)
        method_tag = None
        try:
            method_tag = prep_config_dict['repository_prep']['tag']
        except KeyError:
            msg = "Could not find ['repository_prep']['tag'] in dict: %r"
            msg = msg % (prep_config_dict,)
            raise OPennException(msg)

        return self._prep_methods.get_method_config(method_tag)
