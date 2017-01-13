# -*- coding: utf-8 -*-
import logging
from copy import deepcopy

from openn.openn_exception import OPennException

class ConfigValidator(object):
    logger = logging.getLogger(__name__)

    def __init__(self, validator_dict, configs_dict):
        self._configs_dict = deepcopy(configs_dict)
        self._validations  = deepcopy(validator_dict)

    def validate(self):
        msgs = []
        msgs += self.validate_unique_fields()
        msgs += self.validate_required_fields()

        if len(msgs) > 0:
            msgs = ["    %s" % (x) for x in msgs ]
            msgs.insert(0, "Errors found in configurations:")
            msg = "\n".join(msgs)
            raise OPennException(msg)

    def validate_required_fields(self):
        msgs = []

        for config_dict in self._configs_dict:
            msgs += self.validate_required(config_dict)

        return msgs

    def validate_required(self, config_dict):
        msgs = []

        missing = []
        for field in self._validations['required_fields']:
            if self.is_field_missing(config_dict, field):
                missing.append(field)

        if len(missing) > 0:
            tag = config_dict.get('tag', 'NOTAG')
            msg = "Required field(s) missing from configuration '%s': %s"
            msg = msg % (tag, ", ".join(missing))
            msgs.append(msg)

        return msgs

    def is_field_missing(self, config_dict, key):
        val = config_dict.get(key, None)

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

    def all_values(self, field):
        vals = [ x.get(field, None) for x in self._configs_dict ]

        return [ x for x in vals if x is not None ]

    def _find_dupes(self, all_vals):

        cts = {}
        for val in all_vals:
            cts[val] = cts.get(val, 0) + 1

        dupes = [ (v, cts[v]) for v in cts if cts[v] > 1 ]

        return dupes