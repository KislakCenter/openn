import json

class FileList:
    def __init__(self, file_list_path):
        self.file_list_path = file_list_path
        self.file_list = json.load(open(file_list_path))

    def files(self,type='document'):
        return self.file_list[type]

    @property
    def document_files(self):
        return self.files('document')

    def count(self,type='document'):
        return len(self.files(type))

    def file(self,index,type='document'):
        lst = self.files(type)
        return lst[index] if (lst and len(lst) > index) else None

    def filename(self,index,type='document'):
        file = self.file(index,type)
        return file['filename'] if file else None
