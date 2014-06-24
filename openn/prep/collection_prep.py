from openn.openn_settings import OPennSettings

"""
Parent of collection-specific Prep classes.
"""
class CollectionPrep(OPennSettings):

    def __init__(self, collection):
        OPennSettings.__init__(self,collection)

    def prep_dir(self):
        pass

    
