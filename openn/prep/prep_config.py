import json
from copy import deepcopy

from openn.collections.collection import Collection
from openn.prep.prep_method import PrepMethod
from openn.openn_exception import OPennException

class PrepConfig:
    def __init__(self, prep_config_tag, coll_prep_dict, coll_dict, prep_dict,
                 license_configs):
        "docstring"
        self._prep_config_tag = prep_config_tag
        self._coll_prep_dict  = deepcopy(coll_prep_dict)
        self._collection      = Collection(coll_dict)
        self._prep_method     = PrepMethod(prep_dict)
        self._license_configs = deepcopy(license_configs)

    def collection(self):
        return self._collection

    def prep_method(self):
        return self._prep_method

    def get_collection_prep(self, source_dir, doc):
        return self._prep_method.get_collection_prep(source_dir, doc)

    def prep_class_params(self):
        return self._prep_method.prep_class_params()

    def prep_class_parameter(self, name):
        try:
            return self.prep_class_params()[name]
        except KeyError:
            msg = "Cannot find prep_class_parameter '%s' in dict %s"
            msg = msg % (name, json.dumps(self.prep_class_params))
            raise OPennException(msg)

    def prep_class_name(self):
        return self._prep_method.get_class_name()

    def source_dir_validations(self):
        return self._prep_method.package_validations()

    def image_types(self):
        try:
            return self._coll_prep_dict['image_types']
        except KeyError:
            msg = "Cannot find required PREP_CONFIG parameter 'image_type'"
            msg += " in dict %s"
            msg = msg % (json.dumps(self._coll_prep_dict),)
            raise OPennException(msg)
