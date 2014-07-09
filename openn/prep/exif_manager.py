# -*- coding: utf-8 -*-

from exiftool import ExifTool
import json
import os
import re
import sh
import tempfile

class ExifManager(object):
    xmp_re = re.compile(':')
    newline_re = re.compile('\n')

    def __init__(self):
        self._exiftool = ExifTool()
        self._tempfiles = set()

    def __del__(self):
        self.stop()

    def add_metadata(self,file_list,prop_dict):
        self.start()
        for file in file_list:
            self._add_md_to_file(file, prop_dict)
        self.stop()

    def add_json_metadata(self,file_list,prop_dict):
        self.start()
        for file in file_list:
            self._add_json_md_to_file(file,prop_dict)
        self.stop()

    def _add_json_md_to_file(self,file,prop_dict):
        dct = { 'SourceFile': file }
        dct.update(**prop_dict)
        path = self._to_json_file(dct)
        tags = [ '-json=%s' % path, file ]
        self._exiftool.execute(*tags)

    def _add_md_to_file(self,file,prop_dict):
        tags = self._build_tags(prop_dict)
        tags.append(file)
        self._exiftool.execute(*tags)

    def start(self):
        self._exiftool.start()

    def stop(self):
        self._exiftool.terminate()
        self._cleanup()

    def _build_tags(self,prop_dict):
        tags = []
        for key in prop_dict:
            tags.append(self._build_tag(key,prop_dict.get(key)))
        return tags

    def _build_tag(self,name,value):
        if ExifManager.newline_re.search(value):
            path = self._value_to_file(value)
            return "%s<=%s" % (self._tag(name), path)
        else:
            return "%s=%s" % (self._tag(name), value)

    def _tag(self,name):
        if ExifManager.xmp_re.search(name):
            return "-xmp-%s" % name
        else:
            return "-%s" % name

    def _to_json_file(self,prop_dict):
        f = tempfile.NamedTemporaryFile()
        f.write(json.dumps(prop_dict))
        f.flush()
        f.seek(0)
        self._tempfiles.add(f)
        return f.name

    def _value_to_file(self,value):
        f = tempfile.NamedTemporaryFile()
        f.write(value)
        f.flush()
        f.seek(0)
        self._tempfiles.add(f)
        return f.name

    def _cleanup(self):
        for f in self._tempfiles:
            f.close()
        self._tempfiles.clear()