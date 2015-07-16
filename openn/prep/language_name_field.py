from openn.prep.virtual_field import VirtualField
from openn.prep.langs import *

class LanguageNameField(VirtualField):
    def values(self, validatable_sheet, arg_fields=[]):
        codes = validatable_sheet.values(arg_fields[0])
        return [ lang_english_name(x) for x in codes ]
