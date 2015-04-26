# -*- coding: utf-8 -*-

import os
import logging

from django.template import Context, Template
from django.conf import settings
from django.template.loader import get_template
from operator import itemgetter

from openn.templatetags.openn_filters import *

class Page(object):

    logger = logging.getLogger(__name__)

    def __init__(self,template_name,outdir,**kwargs):
        self.template_name = template_name
        self.template      = get_template(self.template_name)
        self.outdir        = outdir
        self.outfile       = kwargs['outfile'] if 'outfile' in kwargs else None

    def source_path(self):
        for tdir in settings.TEMPLATE_DIRS:
            path = os.path.join(tdir, self.template_name)
            if os.path.exists(path):
                return path

    def outfile_path(self):
        if self.outfile:
            return os.path.join(self.outdir, self.outfile)
        else:
            return os.path.join(self.outdir, self.template_name)

    def ensure_dir(self, dir_path):
        parent = os.path.dirname(dir_path)
        if not os.path.exists(parent):
            self.ensure_dir(parent)
        if not os.path.exists(dir_path):
            os.mkdir(dir_path)
            os.chmod(dir_path, 0775)

    def create_pages(self):
        out_dir = os.path.dirname(self.outfile_path())
        self.ensure_dir(out_dir)
        f = open(self.outfile_path(), 'w+')
        ctx = self.get_context()
        try:
            f.write(self.template.render(ctx).encode('utf-8'))
        finally:
            f.close()
        os.chmod(self.outfile_path(), 0664)

    def is_makeable(self):
        """ Return true if we find a template for the page."""
        return self.template is not None

    def is_needed(self):
        if not self.is_makeable():
            return False

        if os.path.exists(self.outfile_path()):
            source_mtime = os.path.getmtime(self.source_path())
            out_mtime = os.path.getmtime(self.outfile_path())
            return source_mtime >= out_mtime
        else:
            return True


    def get_context(self):
        """By default context is empty. Child classes should override this
        method."""
        return Context({})
