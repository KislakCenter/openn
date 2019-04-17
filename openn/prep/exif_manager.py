# -*- coding: utf-8 -*-

from exiftool import ExifTool
import json
import os
import re
import sh
import subprocess
import tempfile
import logging

from openn.logging.count_logger import CountLogger

from openn.openn_exception import OPennException

class ExifManager(object):
    xmp_re = re.compile(':')
    newline_re = re.compile('\n')
    logger = logging.getLogger(__name__)

    def __init__(self):
        self._exiftool = ExifTool()
        self._tempfiles = set()

    def __del__(self):
        self.stop()

    def serialize_xmp(self, file_list, **kwargs):
        args = {'keep_open': True }
        args.update(kwargs)
        counter = CountLogger(self.logger, file_list)
        counter.count(msg='Serialize XMP', inc=False)
        for path in file_list:
            self.serialize_xmp_one_file(path, **args)
            counter.count(msg="XMP for %s" % (os.path.basename(path), ))
        self.stop()

    def serialize_xmp_one_file(self, path,**kwargs):
        keep_open = kwargs.get('keep_open', False)
        kwargs.pop('keep_open', None)

        if not self._exiftool.running:
            self.start()
        xmp = "%s.xmp" % (path, )
        tags = [ '-tagsFromFile', path, xmp ]
        self._exiftool.execute(*tags)

        if not keep_open:
            self.stop()

    def get_tag(self,tag,file):
        self.start()
        return self._exiftool.get_tag(tag,file)
        self.stop()

    def add_metadata(self,file_list,prop_dict,overwrite_original=False):
        self.start()
        for file in file_list:
            self._add_md_to_file(file, prop_dict, overwrite_original)
        self.stop()

    def add_json_metadata(self,file_list,prop_dict,overwrite_original=False):
        self.start()
        for file in file_list:
            self._add_json_md_to_file(file,prop_dict, overwrite_original)
        self.stop()

    def add_json_one_file(self,filename,prop_dict,**kwargs):
        """
        kwargs can be:

            overwrite_original : True|[False]
            keep_open          : True|[False] (keep exiftool instance running)
        """
        keep_open = kwargs.get('keep_open', False)
        kwargs.pop('keep_open', None)

        if not self._exiftool.running:
            self.start()

        self._add_json_md_to_file(filename,prop_dict,**kwargs)

        if not keep_open:
            self.stop()

    def add_md_one_file(self,filename,prop_dict,**kwargs):
        """
        kwargs can be:

            overwrite_original : True|[False]
            keep_open          : True|[False] (keep exiftool instance running)
        """
        keep_open = kwargs.get('keep_open', False)
        kwargs.pop('keep_open', None)

        if not self._exiftool.running:
            self.start()

        self._add_md_to_file(filename,prop_dict,**kwargs)

        if not keep_open:
            self.stop()


    def _add_json_md_to_file(self,file,prop_dict,overwrite_original=False):
        dct = { 'SourceFile': file }
        dct.update(**prop_dict)
        path = self._to_json_file(dct)
        tags = [ '-json=%s' % path, file ]
        if overwrite_original:
            tags.insert(0, '-overwrite_original')
        return self._exiftool.execute(*tags)

    def _add_md_to_file(self,file,prop_dict,overwrite_original=False):
        tags = self._build_tags(prop_dict)
        if overwrite_original:
            tags.insert(0, '-overwrite_original')
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
            value = prop_dict.get(key)
            if isinstance(value,list) or isinstance(value,tuple):
                for v in value:
                    tags.append(self._build_tag(key,v))
            else:
                tags.append(self._build_tag(key,value))
        return tags

    def _build_tag(self,name,value):
        if ExifManager.newline_re.search(value):
            path = self._value_to_file(value)
            return "%s<=%s" % (self._tag(name), path)
        else:
            return "%s=%s" % (self._tag(name), value.encode('utf-8'))

    def _tag(self,name):
        if ExifManager.xmp_re.search(name):
            return "-xmp-%s" % name
        else:
            return "-%s" % name

    def _to_json_file(self,prop_dict):
        return self._value_to_file(json.dumps(prop_dict))

    def _value_to_file(self,value):
        f = tempfile.NamedTemporaryFile(delete=False)
        f.write(value.encode('utf-8'))
        f.flush()
        f.seek(0)
        name = f.name
        self._tempfiles.add(name)
        return name

    def _cleanup(self):
        for f in self._tempfiles:
            try:
                os.remove(f)
            except OSError:
                pass
        self._tempfiles.clear()
