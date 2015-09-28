from copy import deepcopy

class PrepMethod(object):
    def __init__(self, prep_method_config):
        self._config = deepcopy(prep_method_config)

    def package_validations(self):
        return self._config['package_validation']
