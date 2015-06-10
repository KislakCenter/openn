# -*- coding: utf-8 -*-
import os
import logging
import subprocess
import shutil
import glob
import re

from openn.openn_settings import OPennSettings
from openn.prep.status import Status
from openn.openn_exception import OPennException
from openn.xml.openn_tei import OPennTEI
from openn.prep.package_validation import PackageValidation

"""
Parent of collection-specific Prep classes.
"""
class CollectionPrep(OPennSettings,Status):

    logger = logging.getLogger(__name__)

    def __init__(self, source_dir, collection, document):
        self.source_dir = source_dir
        self.document = document
        self._package_validation = None
        OPennSettings.__init__(self,collection)
        Status.__init__(self,source_dir)
        self._removals = []

    @property
    def basedir(self):
        return os.path.basename(self.source_dir)

    @property
    def removals(self):
        return [x for x in self._removals ]

    @property
    def package_validation(self):
        if not self._package_validation and self.coll.get('package_validation', None):
            self._package_validation =  PackageValidation(**self.coll['package_validation'])
        return self._package_validation

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

    def stage_tiffs(self):
        """Move the TIFF files into the data directory"""
        if not os.path.exists(self.data_dir):
            os.mkdir(self.data_dir)
        tiffs = glob.glob(os.path.join(self.source_dir, '*.tif'))
        for x in tiffs:
           shutil.move(x, self.data_dir)

    def fix_tiff_names(self):
        space_re = re.compile('\s+')
        tiffs = glob.glob(os.path.join(self.source_dir, '*.tif'))
        for tiff in tiffs:
            basename = os.path.basename(tiff)
            if space_re.search(basename):
                new_name = os.path.join(self.source_dir,
                                        space_re.sub('_', basename))
                shutil.move(tiff, new_name)

    def validate(self):
        errors = []
        if self.package_validation:
            errors = self.package_validation.validate(self.source_dir)
        if len(errors) > 0:
            msg = 'Invalid package directory: %s' % (self.source_dir,)
            raise(OPennException('\n'.join([msg] + errors)))

    def write_partial_tei(self, outdir, xml):
        outfile = os.path.join(outdir, 'PARTIAL_TEI.xml')
        f = open(outfile, 'w+')
        try:
            f.write(xml)
            # try to read it
            f.seek(0)
            tei = OPennTEI(f)
            tei.validate()
        except Exception as ex:
            # TODO: rename outfile if error
            raise OPennException("Error creating TEI: %s" % str(ex))
        finally:
            f.close()

        return outfile

    def gen_partial_tei(self):
        raise NotImplementedError

    def regen_partial_tei(self, doc, **kwargs):
        raise NotImplementedError

    def prep_dir(self):

        if self.get_status() >= self.COLLECTION_PREP_COMPLETED:
            self.logger.warning("[%s] Collection prep already completed" % (self.basedir,))
        else:
            if self.get_status() > self.COLLECTION_PREP_PACKAGE_VALIDATED:
                self.logger.warning("[%s] Package directory already validated" % (self.basedir,))
            else:
                self.logger.info("[%s] Validating package directory" % (self.basedir,))
                self.validate()
                self.write_status(self.COLLECTION_PREP_PACKAGE_VALIDATED)

            self._do_prep_dir()
            self._cleanup()
            self.write_status(self.COLLECTION_PREP_COMPLETED)

    def _do_prep_dirs(self):
        pass
