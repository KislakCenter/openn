# -*- coding: utf-8 -*-
import os

from openn.openn_settings import OPennSettings
from openn.prep.status import Status

"""
Parent of collection-specific Prep classes.
"""
class CollectionPrep(OPennSettings,Status):

    def __init__(self, source_dir, collection):
        self.source_dir = source_dir
        OPennSettings.__init__(self,collection)
        Status.__init__(self,source_dir)

    @property
    def basedir(self):
        return os.path.basename(self.source_dir)

    def prep_dir(self):
        self._do_prep_dir()
        self.write_status(self.COLLECTION_PREP_COMPLETED)

    def _do_prep_dirs(self):
        pass
