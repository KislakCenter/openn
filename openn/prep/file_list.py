# -*- coding: utf-8 -*-
import json
import os

"""
A wrapper for accessing and managing the ``file_list.json`` file from
a package directory.

The FileList exposes each individual file as a FileData object.
"""
class FileList:
    """
        A completed file list looks like this.

            {
              "document": [
                {
                  "filename": "data/mscodex1589_wk1_front0001.tif",
                  "image_type": "document",
                  "derivs": {
                    "web": {
                      "path": "data/web/0001_0000_web.jpg",
                      "bytes": 2218,
                      "width": 78,
                      "height": 100
                    },
                    "master": {
                      "path": "data/master/0001_0000.tif",
                      "bytes": 24912,
                      "width": 78,
                      "height": 100
                    },
                    "thumb": {
                      "path": "data/thumb/0001_0000_thumb.jpg",
                      "bytes": 2218,
                      "width": 78,
                      "height": 100
                    }
                  },
                  "label": "Front cover"
                },
                {
                  "filename": "data/mscodex1589_wk1_front0002.tif",
                  "image_type": "document",
                  "derivs": {
                    "web": {
                      "deriv_type": "web",
                      "path": "data/web/0001_0001_web.jpg",
                      "bytes": 1823,
                      "width": 78,
                      "height": 100
                    },
                    "master": {
                      "deriv_type": "master",
                      "path": "data/master/0001_0001.tif",
                      "bytes": 24912,
                      "width": 78,
                      "height": 100
                    },
                    "thumb": {
                      "deriv_type": "master",
                      "path": "data/thumb/0001_0001_thumb.jpg",
                      "bytes": 1823,
                      "width": 78,
                      "height": 100
                    }
                  },
                  "label": "Inside front cover"
                },
                // ...
               ],
              "extra": [
                {
                  "image_type": "extra",
                  "filename": "data/mscodex1589_test ref1_1.tif"
                }
              ]
           }
    """
    DOCUMENT   = 'document'
    EXTRA      = 'extra'
    FILE_TYPES = ( DOCUMENT, EXTRA )

    """
    Wrapper for JSON file list expected by CommonPrep. Input has the
    format below.

        {
            "document": [
                {
                    "filename": "data/mscodex1223_wk1_front0001.tif",
                    "label": "Front cover"
                },
                {
                    "filename": "data/mscodex1223_wk1_front0002.tif",
                    "label": "Inside front cover"
                },
                {
                    "filename": "data/mscodex1223_wk1_front0003.tif",
                    "label": "[Flyleaf 1 recto]"
                },
                {
                    "filename": "data/mscodex1223_wk1_front0004.tif",
                    "label": "[Flyleaf 1 verso]"
                },
                {
                    "filename": "data/mscodex1223_wk1_body0001.tif",
                    "label": "1r"
                },
                {
                    "filename": "data/mscodex1223_wk1_body0002.tif",
                    "label": "1v"
                },
                // ....
                {
                    "filename": "data/mscodex1223_wk1_back0005.tif",
                    "label": "Spine"
                }
            ],
            "extra": [
                {
                    "filename": "data/mscodex1589_test ref1_1.tif"
                }
            ]
        }
    """
    def __init__(self, file_list_path):
        """
        Create a new FileList from the provided ``file_list_path``.
        """
        self.file_list_path = file_list_path
        file_dict = json.load(open(file_list_path))
        self.file_list = {}
        for file_type in FileList.FILE_TYPES:
            self.file_list[file_type] = []
            for fdata in file_dict.get(file_type, []):
                self.file_list[file_type].append(self.FileData(fdata))

    @property
    def types(self):
        return self.file_list.keys()

    @property
    def all_file_data(self):
        return [ fdata for file_type in self.types for fdata in self.files(file_type) ]

    def files(self,type=DOCUMENT):
        """
        Return all FileData instances for the given file `type`.
        """
        return self.file_list[type]

    @property
    def document_files(self):
        """
        Convenience property for ``FileList.files(FileList.DOCUMENT)``.
        """
        return self.files(FileList.DOCUMENT)

    @property
    def file_count(self):
        """Return a count of all the files."""
        return sum([len(fls) for fls in self.file_list.values()])

    @property
    def deriv_count(self):
        """Return count of all derivatives."""
        return sum([fdata.deriv_count for fls in self.file_list.values() for fdata in fls ])
        
    def count(self,type=DOCUMENT):
        return len(self.files(type))

    def file(self,index,type=DOCUMENT):
        lst = self.files(type)
        return lst[index] if (lst and len(lst) > index) else None

    def filename(self,index,type=DOCUMENT):
        if self.file(index,type):
            return self.file(index,type).filename

    @property
    def paths(self):
        """
        Return all image paths for this file list. If there are derivatives,
        all derivative paths are returned. For those files without derivatives,
        the filename will be returned.
        """
        ps = []
        for lst in self.file_list.values():
            for file in lst:
                ps += file.paths

        return ps

    @property
    def data(self):
        d = {}
        for key in self.file_list:
            d[key] = []
            for fdata in self.files(key):
                d[key].append(fdata.data)
        return d

    def __str__(self):
        return json.dumps(self.data)

    class FileData:
        MASTER = 'master'
        WEB    = 'web'
        THUMB  = 'thumb'

        def __init__(self, dict):
            self.data = dict
            if self.data.get('derivs', None) is None:
                self.data['derivs'] = {}

        @property
        def filename(self):
            return self.data.get('filename')

        @property
        def label(self):
            return self.data.get('label')

        @property
        def derivs(self):
            return self.data.get('derivs')

        @property
        def deriv_count(self):
            return len(self.derivs)

        @property
        def paths(self):
            """
            Return all paths for this FileData; if there are derivs, all deriv
            paths are returned; if not, FileData.filename is returned.
            """
            if self.derivs and len(self.derivs) > 0:
                return [ d['path'] for d in self.derivs.values() ]
            else:
                return [ self.filename ]

        def add_deriv(self, path, deriv_type, details={}):
            self.derivs[deriv_type] = { 'deriv_type': deriv_type }
            self.derivs[deriv_type]['path'] = path
            self.derivs[deriv_type].update(details)

        def add_deriv_details(self, deriv_type, details):
            self.derivs[deriv_type].update(details)

        def get_deriv_path(self,deriv_type):
            if self.get_deriv(deriv_type):
                return self.get_deriv(deriv_type).get('path')

        def get_deriv(self,deriv_type):
            """
            Return a dict of details for this deriv:

                {
                    'deriv_type': 'master',
                    'path': 'data/master/0001_0001.tif',
                    'bytes': 4483731844837318,
                    'width': 3239,
                    'height': 4141
                }
            """
            return self.derivs.get(deriv_type)

        def __str__(self):
            return json.dumps(self.data)
