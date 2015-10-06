from openn.openn_exception import OPennException
from copy import deepcopy

class PrepMethods(object):

    def __init__(self, prep_methods_configs):
        self._prep_methods = deepcopy(prep_methods_configs)

    def known_tags(self):
        return [ x.get('tag') for x in self._prep_methods ]

    def get_method_config(self, tag):
        for cfg in self._prep_methods:
            if cfg.get('tag', False) == tag:
                return cfg

        msg = "Could not find prep method for tag '%s' (known %s)"
        msg = msg % (tag, ', '.join(self.known_tags()))
        raise OPennException(msg)
