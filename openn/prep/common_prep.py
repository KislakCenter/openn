import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "openn.settings")
import re

from openn.models import *
from openn.xml.openn_tei import OPennTEI
from openn.openn_exception import OPennException

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

    _required_paths = {
            'data directory':  'data_dir',
            'PARTIAL_TEI.xml': 'tei_path',
            'file_list.json':  'file_list_path'
            }

    def __init__(self,source_dir,config={}):
        self.source_dir    = source_dir
        self.source_dir_re = re.compile('^%s/*' % source_dir)
        self.config        = config
        self.data_dir      = os.path.join(self.source_dir, 'data')
        self.tei_path      = os.path.join(self.source_dir, 'PARTIAL_TEI.xml')
        self.file_list_path = os.path.join(self.source_dir, 'file_list.json')
        self.check_valid()

    @property
    def tei(self):
        if self.openn_tei is None:
            self.openn_tei = OPennTEI(self.tei_path)
        return self.openn_tei

    def create_image_dirs(self):
        for name in 'master web thumb extra'.split():
           dir = os.path.join(self.data_dir, name)
           if not os.path.exists(dir):
               os.mkdir(dir)

    def check_valid(self):
        """ Confirm that the source dir has a data directory, PARTIAL_TEI.xml, and
        file_list.json """
        for name in CommonPrep._required_paths:
            path = getattr(self,CommonPrep._required_paths[name])
            if not os.path.exists(path):
                raise OPennException("No %s found in %s" % (name, self.source_dir))

    def prep_dir(self):
        self.create_image_dirs()
