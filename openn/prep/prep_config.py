import json
from copy import deepcopy
import logging

from openn.repository.repository_wrapper import RepositoryWrapper
from openn.prep.prep_method import PrepMethod
from openn.openn_exception import OPennException

class PrepConfig:

    logger = logging.getLogger(__name__)

    def __init__(self, prep_config_tag, repo_prep_dict, repo_dict, prep_dict,
                 prep_context):
        """
        Create all the information needed for a given repo-prep configuration.

        Parameters
        ----------
        prep_config_tag : str
           The tag for the prep_config; e.g., 'flp-bphil', 'pennmss-pih'.

        repo_prep_dict: dict
            Dict of all repo_preps, linking a repo to prep method,
            containing prep specific parameters

        repo_dict: dict
            Dict of all repository configs

        prep_dict: dict
            Dict of all prep configs

        prep_context: dict
            Dict of context information common to all preps

        The ``prep_context`` looks like this:

                {
                    'archive_dir': ARCHIVE_DIR,
                    'package_dir': PACKAGE_DIR,
                    'staging_dir': STAGING_DIR,
                    'licences': LICENCES,
                    'deriv_configs': DERIV_CONFIGS,
                }
        """
        self._prep_config_tag  = prep_config_tag
        self._repo_prep_dict   = deepcopy(repo_prep_dict)
        self._repo_wrapper     = RepositoryWrapper(repo_dict)
        self._prep_method      = PrepMethod(prep_dict)
        self._prep_class_params = None
        self._context          = deepcopy(prep_context)
        self._rights_dict      = self._repo_prep_dict['rights']
        self._funders = self._repo_prep_dict.get('funders', [])

    def image_rights(self):
        try:
            return self._rights_dict['image_rights']
        except KeyError as kex:
            msg = "Got KeyError (%s) for rights dict: %s"
            raise OPennException(msg % (kex, json.dumps(self._repo_prep_dict)))

    def metadata_rights(self):
        try:
            return self._rights_dict['metadata_rights']
        except KeyError as kex:
            msg = "Got KeyError (%s) for rights dict: %s"
            raise OPennException(msg % (kex, json.dumps(self._repo_prep_dict)))

    def process_directory(self):
        return self.prep_method().process_directory()

    def rights_holder(self):
        if self._rights_dict.get('holder', None) is None:
            return self.repository_wrapper().name()
        else:
            return self._rights_dict.get('holder')

    def rights_more_info(self):
        return self._rights_dict.get('more_information', '')

    def rights_dict(self):
        return self._rights_dict

    def context_var(self, name):
        return self._context[name]

    def repository_wrapper(self):
        return self._repo_wrapper

    def repository(self):
        return self.repository_wrapper().repository()

    def prep_method(self):
        return self._prep_method

    def get_prep_class(self):
        prep_class = self._prep_method.get_prep_class()

        return prep_class

    def funders(self):
        return self._funders

    def prep_class_params(self):
        if self._prep_class_params is None:
            self._prep_class_params = {}
            self._prep_class_params.update(self._prep_method.prep_class_params())
            self._prep_class_params.update(self._repo_prep_dict.get('repository_prep', {}).get('params', {}))
        return self._prep_class_params

    def prep_class_parameter(self, name):
        try:
            return self.prep_class_params()[name]
        except KeyError:
            msg = "Cannot find prep_class_parameter '%s' in dict %s"
            msg = msg % (name, json.dumps(self.prep_class_params()))
            raise OPennException(msg)

    def prep_class_name(self):
        return self._prep_method.get_class_name()

    def source_dir_validations(self):
        return self._prep_method.package_validations()

    def before_scripts(self):
        if self._prep_method is None:
            return []
        if self._prep_method._config is None:
            return []

        return self._prep_method._config.get('before_scripts', [])

    def image_types(self):
        try:
            return self._repo_prep_dict['image_types']
        except KeyError:
            msg = "Cannot find required PREP_CONFIG parameter 'image_type'"
            msg += " in dict %s"
            msg = msg % (json.dumps(self._repo_prep_dict),)
            raise OPennException(msg)
