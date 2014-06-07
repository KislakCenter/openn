import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "openn.settings")

from openn.models import *
from openn.xml.openn_tei import OPennTEI
from openn.openn_exception import OPennException
from openn.prep.file_list import FileList
from openn.prep.package_dir import PackageDir
from openn.models import *

from django.core import serializers
from django.conf import settings


class CommonPrep:
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
        `data/<CALL_NUMBER>_TEI.xml`
      - generate description.html
      - generate browse.html

    """

    def __init__(self,source_dir,collection):
        self.package_dir   = PackageDir(source_dir)
        self.collection    = collection
        self.check_valid()

    @property
    def tei(self):
        if getattr(self, 'openn_tei', None) is None:
            self.openn_tei = OPennTEI(self.package_dir.tei_path)
        return self.openn_tei

    @property
    def files(self):
        if getattr(self, 'file_list', None) is None:
            self.file_list= FileList(self.package_dir.file_list_path)
        return self.file_list

    def record_document(self):
        """ Store this manuscript or book or whatever in the database,
        so we can track it and make sure it's unique."""
        doc = Document(call_number = self.tei.call_number,
                collection = self.collection,
                base_dir = self.package_dir.basedir)
        doc.full_clean()
        doc.save()
        return doc

    def check_valid(self):
        self.package_dir.check_valid()

    def rename_files(self, doc_id):
        """ Using the doc_id rename the existing files giving them sequential
        names following this pattern:

                0001_0001.tif
                0001_0002.tif
                0001_0003.tif
                0001_0004.tif
                ....

        Record the new file names and write them to file_list.json.
        """
        for i in range(self.files.count()):
            curr_name = self.files.filename(i)
            print curr_name
            print self.package_dir.master_name(curr_name, doc_id, i)

    def prep_dir(self):
        doc = self.record_document()
        self.package_dir.create_image_dirs()
        self.rename_files(doc.id)
