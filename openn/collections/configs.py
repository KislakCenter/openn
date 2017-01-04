# -*- coding: utf-8 -*-
import logging
from copy import deepcopy

from openn.openn_exception import OPennException
from openn.collections.collection import Collection
from openn.collections.config_validator import ConfigValidator

class Configs(object):
    logger = logging.getLogger(__name__)

    def __init__(self, coll_configs_dict):
        self._collections_config = deepcopy(coll_configs_dict)

    def tags(self):
        return self.all_values('tag')

    def all_values(self, field):
        vals = [ x.get(field, None) for x in self._configs ]

        return [ x for x in vals if x is not None ]

    def all_collections(self):
        return [ self.get_collection(tag) for tag in self.tags() ]

    def get_collection(self, tag):
        return Collection(self.get_config(tag))

    def get_config(self, tag):
        configlist = [ x for x in self._configs if x['tag'] == tag ]

        if len(configlist) == 1:
            return configlist[0]
        elif len(configlist) > 1:
            msg = "Invalid collections config: more than one has tag '%s'"
            raise OPennException(msg % (tag,))
        else:
            raise OPennException("Unknown tag: '%s'" % (tag,))

    def validate(self):
        validator = ConfigValidator(self._validations, self._configs)
        validator.validate()

    @property
    def _configs(self):
        try:
            return self._collections_config['configs']
        except KeyError:
            msg = "COLLECTIONS config should have key 'configs']"
            raise OPennException(msg)

    @property
    def _validations(self):
        try:
            return self._collections_config['validations']
        except KeyError:
            msg = "COLLECTIONS config should have key 'validations']"
            raise OPennException(msg)
