# -*- coding: utf-8 -*-
import os
import logging
import glob

from openn.models import *
from openn import openn_db
from openn.xml.openn_tei import OPennTEI
from openn.openn_exception import OPennException
from openn.prep.file_list import FileList
from openn.prep.package_dir import PackageDir
from openn.openn_settings import OPennSettings
from openn.prep.status import Status
from openn.prep.license import LicenseFactory
from openn.models import *
import openn.app as op_app

from django.core import serializers

"""
CommonPrep performs OPenn preparation common to all OPenn data packages.

CommonPrep expects an input package to have undergone repository-specific
preparation and to conform to its input requirements, which are described
below.
"""

class CommonPrep(Status):
    """
    Perform common preparation of OPenn data packages, including:
         - Create image directory structure
         - Rename image files
         - Generate suppporting metadata
         - Generate manifest

    CommonPrep expects the following directory structure:

        CALL_NUMBER/
          PARTIAL_TEI.xml # lacks facsimile section
          file_list.json  # list of all files with labels
          data/
            image1.tif
            image2.tif
            ...

    CommonPrep process will take the prepared directory, and

      - rename the files using the project format: (0001_0000.tif,
        0001_0001.tif, 0001_0002.tif, ...)
      - move the files into data/master
      - create thumbnail and web JPEG derivatives in thumb and web, resp.
      - add to the file list the new file names
      - append the facsimile section to the TEI file, outputting
        `data/<DOC_ID>_TEI.xml` (using format "%04d_TEI.xml")
      - generate description.html
      - generate browse.html

    """

    logger = logging.getLogger(__name__)

    def __init__(self,source_dir, document, prep_config):
        Status.__init__(self,source_dir)
        self.source_dir    = source_dir
        self.package_dir   = PackageDir(source_dir)
        self.prep_config   = prep_config
        self.document      = document
        self._removals      = []

    @property
    def tei(self):
        if getattr(self, 'openn_tei', None) is None:
            f = open(self.package_dir.partial_tei_path, 'r')
            try:
                self.openn_tei = OPennTEI(f.read())
            finally:
                f.close()
        return self.openn_tei

    @property
    def files(self):
        if getattr(self, 'file_list', None) is None:
            self.file_list= FileList(self.package_dir.file_list_path)
        return self.file_list

    def add_default_removals(self):
        for x in glob.glob(os.path.join(self.source_dir, '~*')):
            self.add_removal(x)

    def add_removal(self, removal):
        self._removals.append(removal)

    def reset_removals(self):
        self._removals = []

    def save_version(self,doc,attrs={}):
        if doc.version_set.count() > 0:
            version = doc.version_set.last()
            if doc.is_online:
                attrs.update(version.next_patch())
                attrs.setdefault('description', 'Patch revision')
            else:
                attrs.update(version.minor_version)
                attrs.setdefault('description', 'Minor revision' )
        else:
            attrs.setdefault('major_version', 1)
            attrs.setdefault('minor_version', 0)
            attrs.setdefault('patch_version', 0)
            attrs.setdefault('description', 'Initial version')

        return openn_db.save_version(doc,attrs)

    def update_document(self):
        self.document.call_number = self.tei.call_number
        self.document.title = getattr(self.tei, 'title', 'Untitled')
        self.document.save()
        return self.document

    def check_valid(self):
        self.package_dir.check_valid()

    def update_tei(self):
        self.tei.add_file_list(self.document)
        lic_fact = LicenseFactory(op_app.LICENSES)
        self.tei.add_licences(self.document, lic_fact)
        self.tei.add_funders(self.prep_config.funders())
        self.package_dir.save_tei(self.tei, self.document)
        self.document.tei_xml = self.tei.to_string()
        self.document.save()
        self.add_removal(self.package_dir.partial_tei_path)

    def prep_dir(self):
        self.check_valid()

        if self.get_status() < self.REPOSITORY_PREP_COMPLETED:
            raise OPennException("Repository prep not complete")

        basedir = self.package_dir.basedir
        # rename master files
        if self.get_status() > self.MASTERS_RENAMED:
            self.logger.warning("[%s] Master files already renamed", basedir)
        else:
            self.logger.info("[%s] Rename master files", basedir)
            self.package_dir.rename_masters(self.document)
            self.write_status(self.MASTERS_RENAMED)

        # generate derivatives
        if self.get_status() > self.DERIVS_CREATED:
            self.logger.warning("[%s] Derivatives already created", basedir)
        else:
            self.logger.info("[%s] Generate derivatives", basedir)
            self.package_dir.create_derivs(
                self.prep_config.context_var('deriv_configs'))
            openn_db.save_image_data(self.document,self.package_dir.file_list.data)
            self.write_status(self.DERIVS_CREATED)

        # update tei
        if self.get_status() > self.TEI_COMPLETED:
            self.logger.warning("[%s] TEI already completed", basedir)
        else:
            self.logger.info("[%s] Complete TEI", basedir)
            self.update_document()
            self.update_tei()
            self.write_status(self.TEI_COMPLETED)

        # add metadata derivatives
        if self.get_status() > self.IMAGE_METADATA_ADDED:
            self.logger.warning("[%s] Image metadata already added", basedir)
        else:
            self.logger.info("[%s] Add metadata", basedir)
            self.package_dir.add_image_metadata(self.document, LicenseFactory(op_app.LICENSES))
            self.write_status(self.IMAGE_METADATA_ADDED)

        # serialize_xmp
        if self.get_status() > self.IMAGE_DETAILS_UPDATED:
            self.logger.warning("[%s] Image details already updated", basedir)
        else:
            self.logger.info("[%s] Serialize XMP", basedir)
            self.package_dir.serialize_xmp(self.document)
            self.package_dir.update_image_details()
            self.write_status(self.IMAGE_DETAILS_UPDATED)

        # generate manifest
        if self.get_status() > self.MANIFEST_CREATED:
            self.logger.warning("[%s] Manifest already generated", basedir)
        else:
            self.logger.info("[%s] Generate manifest", basedir)
            self.package_dir.create_manifest()
            self.write_status(self.MANIFEST_CREATED)

        # write version.txt
        if self.get_status() > self.VERSION_TXT_WRITTEN:
            self.logger.warning("[%s] Version.txt already written", basedir)
        else:
            self.logger.info("[%s] Write version.txt", basedir)
            version = self.save_version(self.document)
            self.package_dir.write_version_txt(self.document)
            self.write_status(self.VERSION_TXT_WRITTEN)

        if self.get_status() >= self.COMMON_PREP_COMPLETED:
            self.logger.warning("[%s] Common prep already complete", basedir)
        else:
            self.logger.info("[%s] Marking common prep COMPLETED", basedir)
            self.write_status(self.COMMON_PREP_COMPLETED)

        self.add_default_removals()
        self.add_removal(self.package_dir.partial_tei_path)
        self.add_removal(self.package_dir.file_list_path)
        self.add_removal(self.status_file_path)

        self._cleanup()

    def _cleanup(self):
        for r in self._removals:
            if os.path.exists(r):
                self.logger.debug("[%s] Cleanup: removing \'%s\'", self.package_dir, r)
                os.remove(r)
