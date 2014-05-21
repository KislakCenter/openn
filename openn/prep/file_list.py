import json

class FileList:
    def __init__(self, file_list_path):
        self.file_list_path = file_list_path
        self.file_list = json.load(open(file_list_path))
