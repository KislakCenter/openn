from copy import deepcopy
from openn import openn_functions as opfunc

class PrepMethod(object):
    def __init__(self, prep_method_config):
        self._config = deepcopy(prep_method_config)

    def package_validations(self):
        return self._config['package_validation']

    def prep_class_params(self):
        prep_class_dict = self.get_prep_class_config()

        return prep_class_dict.get('params', {})

    def grab_prep_class_param(self, name):
        return self.prep_class_dict[name]

    def process_directory(self):
        return self._config.get('process_directory', True)

    def get_prep_class(self):
        class_name = self.get_class_name()
        return opfunc.get_class(class_name)

    def get_class_name(self):
        prep_class_dict = self.get_prep_class_config()

        return prep_class_dict['class_name']

    def get_prep_class_config(self):
        try:
            return self._config['prep_class']
        except KeyError:
            msg = "Could not find prep_class configuration in method config %r"
            raise OPennException(msg % self._config)
