# -*- coding: utf-8 -*-

import os

from django.template import Context, Template
from django.conf import settings
from django.template.loader import get_template
from operator import itemgetter

from openn.templatetags.openn_filters import *

class Page(object):

    def __init__(self,template_name,outdir,**kwargs):
        self.template_name = template_name
        self.template      = get_template(self.template_name)
        self.outdir        = outdir
        self.outfile       = kwargs['outfile'] if 'outfile' in kwargs else None

    def outfile_path(self):
        if self.outfile:
            return os.path.join(self.outdir, self.outfile)
        else:
            return os.path.join(self.outdir, self.template_name)

    def ensure_dir(self):
        dir = os.path.dirname(self.outfile_path())
        if not os.path.exists(dir):
            os.makedirs(dir)

    def create_pages(self):
        self.ensure_dir()
        f = open(self.outfile_path(), 'w+')
        ctx = self.get_context()
        try:
            f.write(self.template.render(ctx).encode('utf-8'))
        finally:
            f.close()

    def get_context(self):
        pass
