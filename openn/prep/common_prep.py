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
from openn.models import *

from django.core import serializers

"""
CommonPrep performs OPenn preparation common to all OPenn data packages.

CommonPrep expects an input package to have undergone collection-specific
preparation and to conform to its input requirements, which are described
below.
"""

class CommonPrep(OPennSettings):
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
        doc = self.save_document()
        version = self.save_version(doc)
        # rename master files
        self.logger.info("[%s] Rename master files" % (self.package_dir.basedir))
        self.package_dir.rename_masters(doc)

        # generate derivatives
        self.logger.info("[%s] Generate derivatives" % (self.package_dir.basedir))
        self.package_dir.create_derivs(self.deriv_configs)
        openn_db.save_image_data(doc,self.package_dir.file_list.data)

        self.tei.add_file_list(self.package_dir.file_list)
        self.package_dir.save_tei(self.tei, doc)
        doc.tei_xml = self.tei.to_string()
        doc.save()

        # add metadata derivatives
        self.logger.info("[%s] Add metadata" % (self.package_dir.basedir))
        self.package_dir.add_image_metadata(doc,self.coll_config.get('image_rights'))

        # serialize_xmp
        self.logger.info("[%s] Serialize XMP" % (self.package_dir.basedir))
        self.package_dir.serialize_xmp()
        self.package_dir.update_image_details()

        # generate manifest
        self.logger.info("[%s] Generate manifest" % (self.package_dir.basedir))
        self.package_dir.create_manifest()

        # write version.txt
        self.logger.info("[%s] Write version.txt" % (self.package_dir.basedir))
        self.package_dir.write_version_txt(doc)
        self._cleanup()

    def _cleanup(self):
        removals = []
        removals.append(self.package_dir.partial_tei_path)
        removals.append(self.package_dir.file_list_path)
        for r in removals:
            if os.path.exists(r):
                os.remove(r)
