import os
import re

from openn.openn_exception import OPennException
from openn.prep.file_list import FileList
from openn.prep.exif_manager import ExifManager
import openn.prep.image_deriv as image_deriv

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
        self.source_dir_re = re.compile('^%s' % os.path.join(source_dir, '*'))

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
    def file_list(self):
        if getattr(self, '_file_list', None) is None:
            self._file_list = FileList(self.file_list_path)
        return self._file_list

    @property
    def file_list_path(self):
        return os.path.join(self.source_dir, 'file_list.json')

    @property
    def master_dir(self):
        if getattr(self,'_master_dir', None):
            dir = _master_dir
        else:
            dir = os.path.join(self.data_dir, PackageDir.MASTER)
        return self.source_dir_re.sub('', dir)

    @master_dir.setter
    def master_dir(self,path):
        self._master_dir = path

    @master_dir.deleter
    def master_dir(self):
        del(self._master_dir)

    def rename_masters(self, doc_id):
        """ Using the doc_id rename the existing files giving them sequential
        names following this pattern:

                0001_0001.tif
                0001_0002.tif
                0001_0003.tif
                0001_0004.tif
                ....

        Record the new file names and write them to file_list.json.
        """
        self.create_image_dir('master')
        for i in range(self.file_list.count(FileList.DOCUMENT)):
            fdata = self.file_list.file(i, FileList.DOCUMENT)
            curr_name = fdata.filename
            new_name = self.master_name(curr_name, doc_id, i)
            src = os.path.join(self.source_dir, curr_name)
            dst = os.path.join(self.source_dir, new_name)
            os.rename(src, dst)
            details = image_deriv.details(self.source_dir, new_name)
            fdata.add_deriv(new_name, FileList.FileData.MASTER, details)

    def master_name(self,orig,doc_id,index):
        orig_dir = os.path.dirname(orig)
        orig_ext = os.path.splitext(orig)[1]
        new_base = "%04d_%04d%s" % ( doc_id, index, orig_ext )
        return os.path.join(self.master_dir, new_base)

    def create_image_dirs(self):
        for name in self.image_dirs:
           dir = os.path.join(self.data_dir, name)
           if not os.path.exists(dir):
               os.mkdir(dir)

    def create_image_dir(self,deriv_type):
        dir = os.path.join(self.data_dir, deriv_type)
        if not os.path.exists(dir):
            os.mkdir(dir)
        return dir

    def deriv_name(self,master,deriv_type,ext):
        base = os.path.splitext(os.path.basename(master))[0]
        dbase = "%s_%s.%s" % (base, deriv_type, ext)
        return os.path.join('data', deriv_type, dbase)

    def create_derivs(self, deriv_configs):
        """
        Create a deriv for each master file for each configured derivative type
        in deriv_configs.
        Deriv config is a dictionary of values like this:

        {
            'web': {
                'ext': 'jpg',
                'max_side': 1800,

                },
            'thumb': {
                'ext': 'jpg',
                'max_side': 190,
                },
           }

        Derivatives are created for each type, here 'web' and 'thumb'; 'ext'
        gives the file type and extension; 'max_side' gives the maximum number of
        pixels on the derivative image side. Derivatives are only reduced in
        size, never stretched.
        """
        for deriv_type in deriv_configs:
            self.create_image_dir(deriv_type)
            dconf = deriv_configs[deriv_type]
            for fdata in self.file_list.document_files:
                master = fdata.get_deriv_path(FileList.FileData.MASTER)
                deriv = self.deriv_name(master, deriv_type, dconf['ext'])
                details = image_deriv.generate(self.source_dir, master, deriv, dconf['max_side'])
                fdata.add_deriv(deriv, deriv_type, details=details)

    def add_image_metadata(self,md_dict):
        images = []
        files = [ os.path.join(self.source_dir, x) for x in self.file_list.paths ]
        exman = ExifManager()
        exman.add_json_metadata(files, md_dict)
