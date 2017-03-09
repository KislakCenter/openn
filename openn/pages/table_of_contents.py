# -*- coding: utf-8 -*-

import glob
import logging

from django.template import Context, Template
from django.template.loader import get_template

from operator import itemgetter

from openn.models import *
import openn.openn_functions as opfunc
from openn.pages.page import Page
from openn.pages.document_data import DocumentData

class TableOfContents(Page):

    logger = logging.getLogger(__name__)

    def __init__(self, repository,toc_dir,**kwargs):
        self.repository = repository
        self.toc_dir = toc_dir
        kwargs.update({'outfile':self.toc_path(),
                       'page_object': self.repository.repository()})
        super(TableOfContents,self).__init__(**kwargs)

    def get_context(self,ctx_dict={}):
        docs = Document.objects.filter(
            repository=self.repository.repository(),
            is_online=True)
        items = [ DocumentData(x, self.repository, self.toc_dir) for x in docs ]
        ctx = { 'repository': self.repository,
                'items': items }
        ctx.update(ctx_dict={})
        return super(TableOfContents, self).get_context(ctx)

    @property
    def repository_config(self):
        return self.repository.config()

    @property
    def title(self):
        return self.repository_config['name']

    def toc_path(self):
        toc_file = self.repository.toc_file()
        return "%s/%s" % (self.toc_dir, toc_file)

    def is_makeable(self):
        if not self.repository.is_live():
            self.logger.info("TOC not makeable; repository not set to 'live' (repository: %s)" % (
                self.repository.tag()))
            return False

        # If this is a no-document repository, it is makeable; we don't have
        # to look for an `html` dir or the files in it.
        if self.repository.no_document():
            return True

        html_dir = os.path.join(self.outdir, self.repository.html_dir())
        if not os.path.exists(html_dir):
            self.logger.info("TOC not makeable; no HTML dir found: %s (repository: %s)" % (
                html_dir, self.repository.tag()))
            return False

        html_files = glob.glob(os.path.join(html_dir, '*.html'))
        if len(html_files) == 0:
            self.logger.info("TOC not makeable; no HTML files found in %s (repository %s)" % (
                html_dir, self.repository.tag()))
            return False

        return True

    def is_needed(self, strict=True):
        if not self.is_makeable() and strict is True:
            return False

        if not self.output_file_exists():
            return True

        html_dir = os.path.join(self.outdir, self.repository.html_dir())
        html_files = glob.glob(os.path.join(html_dir, '*.html'))
        if html_files:
            newest_html = max([os.path.getmtime(x) for x in html_files])
            if os.path.getmtime(self.outfile_path()) > newest_html:
                logging.info("TOC file newer than all HTML files found in %s; skipping %s" % (html_dir, self.repository.tag()))
                return False

        return True
