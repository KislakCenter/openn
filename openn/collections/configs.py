# -*- coding: utf-8 -*-
import logging
from copy import deepcopy

from openn.openn_exception import OPennException
from openn.collections.collection import Collection

class Configs(object):
    logger = logging.getLogger(__name__)

    def __init__(self, coll_configs_dict):
        self._collections_config = deepcopy(coll_configs_dict)

    def tags(self):
        return self.all_values('tag')

    def all_values(self, field):
        vals = [ x.get(field, None) for x in self._configs ]

        return [ x for x in vals if x is not None ]

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
        msgs = []
        msgs += self.validate_unique_fields()
        msgs += self.validate_required_fields()

        if len(msgs) > 0:
            msgs = ["    %s" % (x) for x in msgs ]
            msgs.insert(0, "Errors found in collection configurations:")
            msg = "\n".join(msgs)
            raise OPennException(msg)

    def validate_required_fields(self):
        msgs = []

        for config in self._configs:
            msgs += self.validate_required(config)

        return msgs

    def validate_required(self, config):
        msgs = []

        missing = []
        for field in self._validations['required_fields']:
            if self.is_field_missing(config, field):
                missing.append(field)

        if len(missing) > 0:
            tag = config.get('tag', 'NOTAG')
            msg = "Required field(s) missing from configuration '%s': %s"
            msg = msg % (tag, ", ".join(missing))
            msgs.append(msg)

        return msgs

    def is_field_missing(self, config, field):
        val = config.get(field, None)

        # no field?
        if val is None:
            return True

        # empty or blank string?
        if isinstance(val, str) or isinstance(val, unicode):
            if len(val.strip()) == 0:
                return True

        return False

    def validate_unique_fields(self):
        msgs = []
        for field in self._validations['unique_fields']:
            msg = self.validate_unique(field)
            if msg is not None:
                msgs.append(msg)

        return msgs

    def validate_unique(self, field):
        msg = None
        all_vals = self.all_values(field)
        vals_set = set(all_vals)

        if len(all_vals) != len(vals_set):
            dupes = self._find_dupes(field)
            text  = '; '.join(["'%s' %dx" % x for x in dupes])
            msg   = "Duplicate values for unique field '%s': %s" % (field,text)

        return msg

    def _find_dupes(self, field):
        all_vals = self.all_values(field)

        cts = {}
        for val in all_vals:
            cts[val] = cts.get(val, 0) + 1

        dupes = [ (v, cts[v]) for v in cts if cts[v] > 1 ]

        return dupes

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
