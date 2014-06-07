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
        if getattr(self, '_image_dirs', None):
            return self._image_dirs
        else:
            return PackageDir.IMAGE_DIRS

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

    @property
    def master_dir(self):
        if getattr(self,'_master_dir', None):
            return _master_dir
        else:
            return os.path.join(self.data_dir, PackageDir.MASTER)

    @master_dir.setter
    def master_dir(self,path):
        self._master_dir = path

    @master_dir.deleter
    def master_dir(self):
        del(self._master_dir)

    def master_name(self,orig,doc_id,index):
        orig_dir = os.path.dirname(orig)
        orig_ext = os.path.splitext(orig)[1]
        new_base = "%04d_%04d.%s" % ( doc_id, index, orig_ext )
        return os.path.join(self.master_dir, new_base)

    def create_image_dirs(self):
        for name in self.image_dirs:
           dir = os.path.join(self.data_dir, name)
           if not os.path.exists(dir):
               os.mkdir(dir)
