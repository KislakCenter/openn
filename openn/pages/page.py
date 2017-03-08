# -*- coding: utf-8 -*-

import os
import logging
from copy import deepcopy

from django.template import Context, Template
from django.template.loader import get_template
from django.conf import settings
from operator import itemgetter
from openn.models import SiteFile

from openn.templatetags.openn_filters import *

class Page(object):

    logger = logging.getLogger(__name__)

    human_name = None

    def __init__(self, template_name, outdir, page_object=None, **kwargs):
        self.template_name = template_name
        self.template      = get_template(self.template_name)
        self.outdir        = outdir
        self._title        = kwargs['title'] if 'title' in kwargs else None
        self.outfile       = kwargs['outfile'] if 'outfile' in kwargs else None
        self.page_object   = page_object
        self.context       = deepcopy(kwargs)
        self.after_writes  = set()
        self.site_file     = None
        self.set_site_file()
        self.add_after_write('update_last_generated')

    @property
    def title(self):
        return self._title

    def add_after_write(self, method_name):
        self.after_writes.add(method_name)

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
        self._do_after_write()

    def is_makeable(self):
        """ Return true if we find a template for the page."""
        return self.template is not None

    def output_file_exists(self):
        if os.path.exists(self.outfile_path()):
            return True
        else:
            logging.info(
                "%s HTML file does not exist: %s",
                self._get_human_name(), self.outfile_path())
            return False

    def template_changed(self):
        if self.site_file.template_has_changed():
            logging.info("%s template file has changed: %s",
                         self._get_human_name(),
                         self.site_file.template_path())
            return True
        else:
            return False

    def changed_since_generation(self, comp_date):
        if self.site_file.last_generated is None:
            logging.info(
                "%s HTML has no last generated date; generating",
                self._get_human_name())
            return True

        # NOT needed if page last generated date is stale
        if self.site_file.last_generated > comp_date:
            logging.info(
                "%s HTML hasn't changed since last generated; skipping",
                self._get_human_name())
            return False

    def include_file_changed(self, page_object):
        if not hasattr(page_object, 'include_file'):
            return False

        if self.site_file.include_file_has_changed():
            logging.info(
                "%s include file has changed: %s",
                self._get_human_name(),
                self.site_file.include_file_path())
            return True

    def is_needed(self, strict=True):
        """ Default is_needed method. Return False if:

            - the page is not makeable
            - the out file already exists, and the template hasn't changed
              since the file was last generated


        """
        if not self.is_makeable() and strict is True:
            return False

        if self.output_file_exists():
            return self.template_changed()

        return True


    def get_context(self, ctx_dict={}):
        """By default context is empty. Child classes should override this
        method."""
        ctx = {'title': self.title, 'context': self.context}
        ctx.update(ctx_dict)
        return Context(ctx)

    def set_site_file(self):
        if self.outfile is None:
            self.site_file = SiteFile.find_or_create(self.template_name)
        else:
            self.site_file = SiteFile.find_or_create(self.outfile)
        if self.template_name is not None:
            self.site_file.set_template(self.template_name)
        if self.include_file() is not None:
            self.site_file.set_include_file(self.include_file())

    def update_last_generated(self):
        "Update the last generated date on the site_file"
        self.site_file.update_last_generated()

    def include_file(self):
        "Return the include file if self.page_object exists and has one."
        if hasattr(self.page_object, 'include_file'):
            return self.page_object.include_file

    def update_hashes(self):
        if self.site_file is None:
            return

        if self.site_file.template is not None:
            self.site_file.update_template_sha256()

        if self.site_file.include_file is not None:
            self.site_file.update_include_file_sha256()

    def _get_human_name(self):
        if self.human_name is None:
            return type(self).__name__
        else:
            return self.human_name

    def _do_after_write(self):
        for meth in self.after_writes:
            getattr(self, meth)()
