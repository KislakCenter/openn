import os
import re

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
    def __init__(self,source_dir,config={}):
        self.source_dir    = source_dir
        self.source_dir_re = re.compile('^%s/*' % source_dir)
        self.config        = config
        self.data_dir      = os.path.join(self.source_dir, 'data')
        if not os.path.exists(self.data_dir):
            raise OPennException("No data directory found in %s" % self.source_dir)

    def create_image_dirs(self):
        for name in 'master web thumb extra'.split():
           dir = os.path.join(self.data_dir, name)
           if not os.path.exists(dir):
               os.mkdir(dir)

    def prep_dir(self):
        self.create_image_dirs()
