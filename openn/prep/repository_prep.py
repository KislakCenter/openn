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
from openn.openn_functions import *


"""
Parent of repository-specific Prep classes.
"""
class RepositoryPrep(Status):

    logger = logging.getLogger(__name__)

    def __init__(self, source_dir, document, prep_config):
        self.source_dir = source_dir
        self.partial_tei_file = os.path.join(self.source_dir, 'PARTIAL_TEI.xml')
        self.document = document
        self.prep_config = prep_config
        self._package_validation = PackageValidation(
            **self.prep_config.source_dir_validations())
        self.encoding_desc_path = prep_config.prep_class_params().get('encoding_desc', None)
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
        return self._package_validation

    def keywords_filename(self):
        return os.path.join(self.source_dir, 'keywords.txt')

    def add_removals(self, removals):
        for removal in removals:
            self.add_removal(removal)

    def add_removal(self, removal):
        if removal is None:
            return
        self._removals.append(removal)

    def reset_removals(self):
        self._removals = []

    def _cleanup(self):
        for f in self.removals:
            if os.path.exists(f):
                self.logger.debug("[%s] Cleanup: removing \'%s\'",
                    self.basedir,f)
                os.remove(f)

    def image_files(self,image_dir=None):
        images = []

        image_dir = image_dir if image_dir else self.source_dir
        for g in self.prep_config.image_types():
            images.extend(glob.glob(os.path.join(image_dir, g)))
        return images

    def stage_images(self):
        """Move the TIFF files into the data directory"""
        if not os.path.exists(self.data_dir):
            os.mkdir(self.data_dir)
        for x in self.image_files():
           shutil.move(x, self.data_dir)

    def fix_image_names(self):
        space_re = re.compile('\s+')
        for x in self.image_files():
            basename = os.path.basename(x)
            if space_re.search(basename):
                new_name = os.path.join(self.source_dir,
                                        space_re.sub('_', basename))
                shutil.move(x, new_name)

    def save_rights_data(self):
        self.document.image_licence = self.prep_config.image_rights()
        if not self.prep_config.image_rights().startswith('PD'):
            self.document.image_copyright_holder = self.prep_config.rights_holder()
            self.document.image_copyright_year = datetime.now(pytz.UTC).year
            self.document.image_rights_more_info = self.prep_config.rights_more_info()
        else:
            self.document.image_copyright_holder = None
            self.document.image_copyright_year = None
            self.document.image_rights_more_info = None

        self.document.metadata_licence = self.prep_config.metadata_rights()
        if not self.prep_config.metadata_rights().startswith('PD'):
            self.document.metadata_copyright_holder = self.prep_config.rights_holder()
            self.document.metadata_copyright_year = datetime.now(pytz.UTC).year
            self.document.metadata_rights_more_info = self.prep_config.rights_more_info()
        else:
            self.document.metadata_copyright_holder = None
            self.document.metadata_copyright_year = None
            self.document.metadata_rights_more_info = None

        self.document.save()

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
        finally:
            f.close()

        return outfile

    def build_partial_tei(self):
        xml_string = self.gen_partial_tei()
        tei = OPennTEI(xml_string)
        self.add_keywords(tei)
        self.add_encoding_desc(tei)
        return tei.to_string()

    def gen_partial_tei(self):
        raise NotImplementedError

    def regen_partial_tei(self, doc, **kwargs):
        raise NotImplementedError

    def add_encoding_desc(self, openn_tei):
        """
        If encoding_desc_path is defined and the TEI file has

            profileDesc/textClass/keywords[@n="keywords"]

        then, add the encodingDesc to the partial TEI.
        """
        if len(openn_tei.keywords) > 0:
            if self.encoding_desc_path is not None and self.encoding_desc_path.strip() != '':
                if not os.path.exists(self.encoding_desc_path):
                    raise OPennException("TEI encodingDesc file not found: '%s'" % self.encoding_desc_path)
                openn_tei.add_encoding_desc(open(self.encoding_desc_path).read())

    def add_keywords(self, openn_tei):
        """
        If keywords.txt file is present, add keywords to the TEI header.

        <profileDesc>
            <textClass>
                <keywords n="keywords">
                    <term>15th century</term>
                    <term>Italy</term>
                    <term>Italian</term>
                    <term>Commentary</term>
                    <term>Illumination</term>
                </keywords>
            </textClass>
        </profileDesc>
        """
        if os.path.exists(self.keywords_filename()):
            terms = []
            for x in open(self.keywords_filename()).readlines():
                if len(x.strip()) > 0:
                    terms.append(x.strip())

            if len(terms) > 0:
                openn_tei.add_keywords(terms)

    def validate_partial_tei(self):
        validate_cmd = 'op-vldt-tei'
        p = subprocess.Popen([validate_cmd, self.partial_tei_file],
                             stderr=subprocess.PIPE,
                             stdout=subprocess.PIPE)
        out, err = p.communicate()
        if p.returncode != 0:
            raise OPennException(u"TEI validation failed: %s; returncode: %d" % (err.decode('utf-8'),p.returncode))

        return out

    def prep_dir(self):

        if self.get_status() >= self.REPOSITORY_PREP_COMPLETED:
            self.logger.warning("[%s] Repository prep already completed", self.basedir,)
        else:
            if self.get_status() > self.REPOSITORY_PREP_PACKAGE_VALIDATED:
                self.logger.warning("[%s] Package directory already validated", self.basedir,)
            else:
                self.logger.info("[%s] Validating package directory", self.basedir,)
                self.validate()
                self.write_status(self.REPOSITORY_PREP_PACKAGE_VALIDATED)

            self._do_prep_dir()
            self._cleanup()
            self.write_status(self.REPOSITORY_PREP_COMPLETED)

    def _do_prep_dir(self):
        pass
