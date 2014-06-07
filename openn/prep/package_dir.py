import os
import re

from openn.openn_exception import OPennException

class PackageDir:

    MASTER     = 'master'
    WEB        = 'web'
    THUMB      = 'thumb'
    EXTRA      = 'extra'
    DOCUMENT   = 'document'
    IMAGE_DIRS = ( MASTER, WEB, THUMB, EXTRA )

    # A list of names and path attributes required for a valid source_dir.
    # E.g., the "data directory" should be assigned to the attribute `data_dir`
    # and should existon the file system. The method `check_valid` uses these
    # values to test source validity.
    _required_paths = {
            'data directory':  'data_dir',
            'PARTIAL_TEI.xml': 'tei_path',
            'file_list.json':  'file_list_path'
            }

    def __init__(self, source_dir):
        self.source_dir = source_dir
        self.source_dir_re = re.compile('^%s/*' % source_dir)

    def check_valid(self):
        """ Confirm that the source dir has a data directory, PARTIAL_TEI.xml, and
        file_list.json """
        for name in PackageDir._required_paths:
            path = getattr(self,PackageDir._required_paths[name])
            if not os.path.exists(path):
                raise OPennException("No %s found in %s" % (name, self.source_dir))

    @property
    def data_dir(self):
        return os.path.join(self.source_dir, 'data')

    @property
    def basedir(self):
        return os.path.basename(self.source_dir)

    @property
    def image_dirs(self):
        return self._image_dirs if self._image_dirs else CommonPrep.IMAGE_DIRS

    @image_dirs.setter
    def image_dirs(self,dirs):
        self._image_dirs = dirs

    @image_dirs.deleter
    def image_dirs(self):
        del(self._image_dirs)

    @property
    def tei_path(self):
        return os.path.join(self.source_dir, 'PARTIAL_TEI.xml')

    @property
    def file_list_path(self):
        return os.path.join(self.source_dir, 'file_list.json')

    def create_image_dirs(self):
        for name in 'master web thumb extra'.split():
           dir = os.path.join(self.data_dir, name)
           if not os.path.exists(dir):
               os.mkdir(dir)
