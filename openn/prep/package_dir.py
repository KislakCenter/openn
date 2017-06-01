# -*- coding: utf-8 -*-
import logging
import os
import re
import hashlib
from copy import deepcopy

from openn.openn_exception import OPennException
from openn.prep.file_list import FileList
from openn.prep.exif_manager import ExifManager
from openn.md.image_dc import ImageDC
from openn.md.image_rights import ImageRights
from openn.logging.count_logger import CountLogger
import openn.prep.image_deriv as image_deriv

class PackageDir:

    logger = logging.getLogger(__name__)

    MASTER     = 'master'
    WEB        = 'web'
    THUMB      = 'thumb'
    EXTRA      = 'extra'
    DOCUMENT   = 'document'
    IMAGE_DIRS = ( MASTER, WEB, THUMB )

    # All white space in filenames will be replace by '_' or removed
    white_space_re = re.compile('\s')

    # A list of names and path attributes required for a valid source_dir.
    # E.g., the "data directory" should be assigned to the attribute `data_dir`
    # and should existon the file system. The method `check_valid` uses these
    # values to test source validity.
    _required_paths = {
            'data directory':  'data_dir',
            'PARTIAL_TEI.xml': 'partial_tei_path',
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
    def partial_tei_path(self):
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

    def rename_masters(self, doc):
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
            new_name = self.master_name(curr_name, doc.id, i)
            src = os.path.join(self.source_dir, curr_name)
            dst = os.path.join(self.source_dir, new_name)
            os.rename(src, dst)
            os.chmod(dst, 0664)
            details = image_deriv.details(self.source_dir, new_name)
            fdata.add_deriv(new_name, FileList.FileData.MASTER, details)

        extra_files = self.file_list.files(FileList.EXTRA)
        if extra_files and len(extra_files) > 0:
            self.create_image_dirs(suppl='extra')

        for fdata in extra_files:
            curr_name = fdata.filename
            new_name = self.extra_filename(curr_name)
            src = os.path.join(self.source_dir, curr_name)
            dst = os.path.join(self.source_dir, new_name)
            os.rename(src, dst)
            os.chmod(dst, 0664)
            details = image_deriv.details(self.source_dir, new_name)
            fdata.add_deriv(new_name, FileList.FileData.MASTER, details)

    def extra_filename(self,curr_name):
        base  = os.path.basename(curr_name)
        new_base = PackageDir.white_space_re.sub('_', base)
        return self.source_dir_re.sub('', os.path.join(self.data_dir, 'extra', 'master', new_base))

    def save_tei(self, openn_tei, doc):
        """
        Save openn_tei content to path returned by tei_name()
        """
        if not os.path.exists(self.data_dir):
            os.mkdir(self.data_dir)

        f = open(self.tei_name(doc), 'w+')
        try:
            f.write(openn_tei.to_string())
            self.logger.info("Wrote TEI: '%s'", self.tei_name(doc))
        finally:
            f.close()

    def tei_name(self,doc):
        """ TEI file name is:

               "<data_dir>/%04d_TEI.xml" % doc_id

        """
        return os.path.join(self.data_dir, doc.tei_basename)

    def manifest_path(self):
        return os.path.join(self.source_dir, 'manifest-sha1.txt')

    def version_txt_path(self):
        return os.path.join(self.source_dir, 'version.txt')

    def master_name(self,orig,doc_id,index):
        orig_dir = os.path.dirname(orig)
        orig_ext = os.path.splitext(orig)[1]
        new_base = "%04d_%04d%s" % ( doc_id, index, orig_ext )
        return os.path.join(self.master_dir, new_base)

    def create_image_dirs(self,suppl=None):
        """By default, create image derivatives dirs in <DATA_DIR>. If suppl
        is provided, create suppl dir <DATA_DIR>/suppl, and then
        create the derivative dirs in <DATA_DIR>/suppl.

        """
        data_dir = self.data_dir
        if suppl:
            data_dir = os.path.join(self.data_dir, suppl)

        if not os.path.exists(data_dir):
            os.mkdir(data_dir)

        for name in self.image_dirs:
           dir = os.path.join(data_dir, name)
           if not os.path.exists(dir):
               os.mkdir(dir)

    def create_image_dir(self,deriv_type):
        dir = os.path.join(self.data_dir, deriv_type)
        if not os.path.exists(dir):
            os.mkdir(dir)
        return dir

    def deriv_name(self,master,deriv_type,ext,deriv_dir=None):
        if deriv_dir is None:
            deriv_dir = deriv_type
        base = os.path.splitext(os.path.basename(master))[0]
        dbase = "%s_%s.%s" % (base, deriv_type, ext)
        return os.path.join('data', deriv_dir, dbase)

    def rel_path(self, path):
        return self.source_dir_re.sub('', path)

    def get_sha1(self, path):
        sha1 = hashlib.sha1()
        f = open(path, 'rb')
        try:
            sha1.update(f.read())
        finally:
            f.close()

        return sha1.hexdigest()

    def create_manifest(self):
        manifest = open(self.manifest_path(), 'w+')

        try:
            for root, dirs, files in os.walk(self.data_dir):
                for name in files:
                    path = os.path.join(root, name)
                    manifest.write("%s  %s\n" % (self.get_sha1(path), self.rel_path(path)))
        finally:
            manifest.close()

    def write_version_txt(self, doc):
        version_txt = open(self.version_txt_path(), 'w+')

        try:
            for version in doc.version_set.order_by('-order'):
                version_txt.write('version: %s\n' % (version.text,))
                # date format: YYYY-MM-DDThh:mm:ssTZD
                version_txt.write('date: %s\n' % (version.created.strftime('%Y-%m-%dT%H:%M:%S%z'), ))
                version_txt.write('id: %s\n' % (version.id, ))
                version_txt.write('document: %s\n' % (doc.id, ))
                version_txt.write('\n')
                version_txt.write('%s\n' % (version.description, ))
                version_txt.write('---\n')

        finally:
            version_txt.close()

    def create_derivs(self, deriv_configs,deriv_dir=None):
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

        If deriv_dir is specified, all images will be written to
        'data/<deriv_dir>'; e.g., 'data/extra'. Otherwise, all images will be
        written to the deriv_type dir: 'data/web', 'data/thumb'.
        Derivatives are created for each type, here 'web' and 'thumb'; 'ext'
        gives the file type and extension; 'max_side' gives the maximum number of
        pixels on the derivative image side. Derivatives are only reduced in
        size, never stretched.
        """
        for deriv_type in deriv_configs:
            self.create_image_dir(deriv_type)
            dconf = deriv_configs[deriv_type]
            cntr = CountLogger(self.logger, self.file_list.document_files)
            cntr.count(msg="Generating %s derivatives for document images" % (deriv_type,), inc=False)
            for fdata in self.file_list.document_files:
                master = fdata.get_deriv_path(FileList.FileData.MASTER)
                cntr.count("Generating %s derivative for %s" % (deriv_type,master))
                deriv = self.deriv_name(master, deriv_type, dconf['ext'])
                details = image_deriv.generate(self.source_dir, master, deriv, dconf['max_side'])
                fdata.add_deriv(deriv, deriv_type, details=details)

            cntr = CountLogger(self.logger, self.file_list.extra_files)
            cntr.count(msg="Generating %s derivatives for extra images" % (deriv_type,), inc=False)
            for fdata in self.file_list.extra_files:
                extra_dir = os.path.join('extra', deriv_type)
                master = fdata.get_deriv_path(FileList.FileData.MASTER)
                cntr.count("Generating %s derivative for %s" % (deriv_type,master))
                deriv = self.deriv_name(master, deriv_type, dconf['ext'], deriv_dir=extra_dir)
                details = image_deriv.generate(self.source_dir, master, deriv, dconf['max_side'])
                fdata.add_deriv(deriv, deriv_type, details=details)

    def update_image_details(self):
        for fdata in self.file_list.all_file_data:
            if len(fdata.derivs) > 0:
                for deriv in fdata.derivs.values():
                    details = image_deriv.details(self.source_dir, deriv['path'])
                    deriv.update(details)

    def serialize_xmp(self, doc):
        files = []
        for image in doc.image_set.all():
            for deriv in image.derivative_set.all():
                path = os.path.join(self.source_dir, deriv.path)
                files.append(path)
        exman = ExifManager()
        exman.serialize_xmp(files)
        exman.stop()

    def add_image_metadata(self, doc, license_factory):
        """Add metadata to all images; parameters: ``doc`` -- the document
        object, ``license_factory`` LicenseFactory instance

        """
        images = []
        files = [ os.path.join(self.source_dir, x) for x in self.file_list.paths ]
        exman = ExifManager()
        all_images = doc.image_set.all()
        cntr = CountLogger(self.logger,all_images)
        cntr.count(msg='Adding metadata', inc=False)
        license = license_factory.license(doc.image_licence)
        for image in all_images:
            rights = ImageRights(image, license)
            rights_dict = rights.rights_properties()

            for deriv in image.derivative_set.all():
                fpath = os.path.join(self.source_dir, deriv.path)
                deriv_md = ImageDC(deriv).to_dict()
                deriv_md.update(rights_dict)
                exman.add_md_one_file(fpath, deriv_md, overwrite_original=True, keep_open=True)
            cntr.count("Added metadata to derivatives for %s %s" % (image.master().basename(), image.label))
        exman.stop()
