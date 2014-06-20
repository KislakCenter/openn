import json
import os

"""
A wrapper for accessing and managing the ``file_list.json`` file from
a package directory.

The FileList exposes each individual file as a FileData object.
"""
class FileList:
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

    def count(self,type=DOCUMENT):
        return len(self.files(type))

    def file(self,index,type=DOCUMENT):
        lst = self.files(type)
        return lst[index] if (lst and len(lst) > index) else None

    def filename(self,index,type=DOCUMENT):
        if self.file(index,type):
            return self.file(index,type).filename

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

        def add_deriv(self, path, deriv_type):
            self.derivs[deriv_type] = path

        def get_deriv(self,deriv_type):
            return self.derivs.get(deriv_type)

        def __str__(self):
            return json.dumps(self.data)
