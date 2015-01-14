# -*- coding: utf-8 -*-
import os

class Status(object):
    PREP_BEGUN                          = 0
    COLLECTION_PREP_BEGUN               = 10
    COLLECTION_PREP_PACKAGE_VALIDATED   = 17
    COLLECTION_PREP_MD_VALIDATED        = 25
    COLLECTION_PREP_FILES_VALIDATED     = 40
    COLLECTION_PREP_FILES_STAGED        = 55
    COLLECTION_PREP_FILE_LIST_WRITTEN   = 70
    COLLECTION_PREP_PARTIAL_TEI_WRITTEN = 85
    COLLECTION_PREP_COMPLETED           = 100
    MASTERS_RENAMED                     = 110
    DERIVS_CREATED                      = 120
    TEI_COMPLETED                       = 130
    IMAGE_METADATA_ADDED                = 140
    IMAGE_DETAILS_UPDATED               = 150
    MANIFEST_CREATED                    = 160
    VERSION_TXT_WRITTEN                 = 170
    COMMON_PREP_COMPLETED               = 200

    STATUS_NAMES = {
        0:    'PREP_BEGUN',
        10:   'COLLECTION_PREP_BEGUN',
        17:   'COLLECTION_PREP_PACKAGE_VALIDATED',
        25:   'COLLECTION_PREP_MD_VALIDATED',
        40:   'COLLECTION_PREP_FILES_VALIDATED',
        55:   'COLLECTION_PREP_FILES_STAGED',
        70:   'COLLECTION_PREP_FILE_LIST_WRITTEN',
        85:   'COLLECTION_PREP_PARTIAL_TEI_WRITTEN',
        100:  'COLLECTION_PREP_COMPLETED',
        110:  'MASTERS_RENAMED',
        120:  'DERIVS_CREATED',
        130:  'TEI_COMPLETED',
        140:  'IMAGE_METADATA_ADDED',
        150:  'IMAGE_DETAILS_UPDATED',
        160:  'MANIFEST_CREATED',
        170:  'VERSION_TXT_WRITTEN',
        200:  'COMMON_PREP_COMPLETED'
    }

    FILE_NAME = 'status.txt'

    def __init__(self, source_dir):
        self._source_dir = source_dir

    @property
    def status_file_name(self):
        if getattr(self, '_status_file_name', None):
            return self._status_file_name
        else:
            return Status.FILE_NAME

    @status_file_name.setter
    def status_file_name(self,name):
        self._status_file_name = name

    @status_file_name.deleter
    def status_file_name(self):
        del(self._status_file_name)

    @property
    def status_file_path(self):
        return os.path.join(self._source_dir, self.status_file_name)

    def write_status(self,code):
        with open(self.status_file_path, 'w+') as f:
            f.write("%d %s" % (code, self.STATUS_NAMES[code]))

    def get_status(self):
        code = 0
        if os.path.exists(self.status_file_path):
            with open(self.status_file_path, 'r') as f:
                status = f.read()
                code = int(status.split()[0])
        return code

    def has_status(self,code):
        return self.get_status() == code
