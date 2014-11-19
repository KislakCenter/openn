# -*- coding: utf-8 -*-
import os
import logging

from openn.models import *
from openn import openn_db
from openn.xml.openn_tei import OPennTEI
from openn.openn_exception import OPennException
from openn.prep.file_list import FileList
from openn.prep.package_dir import PackageDir
from openn.openn_settings import OPennSettings
from openn.prep.status import Status
from openn.models import *

from django.core import serializers

"""
CommonPrep performs OPenn preparation common to all OPenn data packages.

CommonPrep expects an input package to have undergone collection-specific
preparation and to conform to its input requirements, which are described
below.
"""

class CommonPrep(OPennSettings,Status):
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

    def __init__(self,source_dir,collection):
        OPennSettings.__init__(self,collection)
        Status.__init__(self,source_dir)
        self.package_dir   = PackageDir(source_dir)
        self.collection    = collection
        self.check_valid()

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

    def save_version(self,doc,attrs={}):
        attrs.setdefault('major_version', 1)
        attrs.setdefault('minor_version', 0)
        attrs.setdefault('patch_version', 0)
        attrs.setdefault('description', 'Initial version')
        return openn_db.save_version(doc,attrs)

    def prep_document(self):
        doc = None
        try:
            attrs = {
                'collection': self.collection,
                'base_dir': self.package_dir.basedir
            }
            doc = Document.objects.get(**attrs)
        except Document.DoesNotExist:
            doc = self.save_document()
        return doc

    def save_document(self):
        """ Store this manuscript or book or whatever in the database,
        so we can track it and make sure it's unique."""
        doc = openn_db.save_document({
            'call_number': self.tei.call_number,
            'collection': self.collection,
            'base_dir': self.package_dir.basedir,
            'title': getattr(self.tei, 'title', 'Untitled')
            })

        return doc

    def check_valid(self):
        self.package_dir.check_valid()

    def prep_dir(self):
        if self.get_status() < self.COLLECTION_PREP_COMPLETED:
            raise OPennException("Collection prep not complete")
        doc = self.prep_document()

        basedir = self.package_dir.basedir
        # rename master files
        if self.get_status() > self.MASTERS_RENAMED:
            self.logger.warning("[%s] Master files already renamed" % (basedir,))
        else:
            self.logger.info("[%s] Rename master files" % (basedir,))
            self.package_dir.rename_masters(doc)
            self.write_status(self.MASTERS_RENAMED)

        # generate derivatives
        if self.get_status() > self.DERIVS_CREATED:
            self.logger.warning("[%s] Derivatives already created" % (basedir,))
        else:
            self.logger.info("[%s] Generate derivatives" % (basedir,))
            self.package_dir.create_derivs(self.deriv_configs)
            openn_db.save_image_data(doc,self.package_dir.file_list.data)
            self.write_status(self.DERIVS_CREATED)

        # generate derivatives
        if self.get_status() > self.TEI_COMPLETED:
            self.logger.warning("[%s] TEI already completed" % (basedir,))
        else:
            self.logger.info("[%s] Complete TEI" % (basedir,))
            self.tei.add_file_list(doc)
            self.package_dir.save_tei(self.tei, doc)
            doc.tei_xml = self.tei.to_string()
            doc.save()
            self.write_status(self.TEI_COMPLETED)

        # add metadata derivatives
        if self.get_status() > self.IMAGE_METADATA_ADDED:
            self.logger.warning("[%s] Image metadata already added" % (basedir,))
        else:
            self.logger.info("[%s] Add metadata" % (basedir,))
            self.package_dir.add_image_metadata(doc,self.coll_config.get('image_rights'))
            self.write_status(self.IMAGE_METADATA_ADDED)

        # serialize_xmp
        if self.get_status() > self.IMAGE_DETAILS_UPDATED:
            self.logger.warning("[%s] Image details already updated" % (basedir,))
        else:
            self.logger.info("[%s] Serialize XMP" % (basedir,))
            self.package_dir.serialize_xmp(doc)
            self.package_dir.update_image_details()
            self.write_status(self.IMAGE_DETAILS_UPDATED)

        # generate manifest
        if self.get_status() > self.MANIFEST_CREATED:
            self.logger.warning("[%s] Manifest already generated" % (basedir,))
        else:
            self.logger.info("[%s] Generate manifest" % (basedir,))
            self.package_dir.create_manifest()
            self.write_status(self.MANIFEST_CREATED)

        # write version.txt
        if self.get_status() > self.VERSION_TXT_WRITTEN:
            self.logger.warning("[%s] Version.txt already written" % (basedir,))
        else:
            self.logger.info("[%s] Write version.txt" % (basedir,))
            version = self.save_version(doc)
            self.package_dir.write_version_txt(doc)
            self.write_status(self.VERSION_TXT_WRITTEN)

        if self.get_status() > self.COMMON_PREP_COMPLETED:
            self.logger.warning("[%s] Common prep already complete" % (basedir,))
        else:
            self.logger.info("[%s] Marking common prep COMPLETED" % (basedir,))

        self._cleanup()

    def _cleanup(self):
        removals = []
        removals.append(self.package_dir.partial_tei_path)
        removals.append(self.package_dir.file_list_path)
        removals.append(self.status_file_path)
        for r in removals:
            if os.path.exists(r):
                self.logger.debug("[%s] Cleanup: removing \'%s\'" % (
                    self.package_dir.basedir,r))
                os.remove(r)
