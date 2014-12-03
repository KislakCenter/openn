# -*- coding: utf-8 -*-
import os
import logging
import subprocess

from openn.openn_settings import OPennSettings
from openn.prep.status import Status
from openn.openn_exception import OPennException
from openn.xml.openn_tei import OPennTEI

"""
Parent of collection-specific Prep classes.
"""
class CollectionPrep(OPennSettings,Status):

    logger = logging.getLogger(__name__)

    def __init__(self, source_dir, collection, document):
        self.source_dir = source_dir
        self.document = document
        OPennSettings.__init__(self,collection)
        Status.__init__(self,source_dir)
        self._removals = []

    @property
    def basedir(self):
        return os.path.basename(self.source_dir)

    @property
    def removals(self):
        return [x for x in self._removals ]

    def add_removals(self, removals):
        for removal in removals:
            self.add_removal(removal)

    def add_removal(self, removal):
        self._removals.append(removal)

    def reset_removals(self):
        self._removals = []

    def _cleanup(self):
        for f in self.removals:
            if os.path.exists(f):
                os.remove(f)

    def write_partial_tei(self, outdir, xml):
        outfile = os.path.join(outdir, 'PARTIAL_TEI.xml')
        f = open(outfile, 'w+')
        try:
            f.write(xml)
            # try to read it
            f.seek(0)
            OPennTEI(f)
        except Exception as ex:
            # TODO: rename outfile if error
            raise OPennException("Error creating TEI: %s" % str(ex))
        finally:
            f.close()

        return outfile

    def gen_partial_tei(self):
        raise NotImplementedError

    def prep_dir(self):
        if self.get_status() >= self.COLLECTION_PREP_COMPLETED:
            self.logger.warning("[%s] Collection prep already completed" % (self.basedir,))
        else:
            self._do_prep_dir()
            self.write_status(self.COLLECTION_PREP_COMPLETED)
            self._cleanup()

    def _do_prep_dirs(self):
        pass
