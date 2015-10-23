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

    def __init__(self, collection,toc_dir,**kwargs):
        self.collection = collection
        self.toc_dir = toc_dir
        updated_kwargs = kwargs.update({'outfile':self.toc_path()})
        super(TableOfContents,self).__init__(**kwargs)


    def get_context(self,ctx_dict={}):
        docs = Document.objects.filter(
            openn_collection=self.collection.openn_collection(),
            is_online=True)
        items = [ DocumentData(x, self.collection, self.toc_dir) for x in docs ]
        ctx = { 'collection': self.collection,
                'items': items }
        ctx.update(ctx_dict={})
        return super(TableOfContents, self).get_context(ctx)

    @property
    def collection_config(self):
        return self.collection.config()

    @property
    def title(self):
        return self.collection_config['name']

    def toc_path(self):
        toc_file = self.collection.toc_file()
        return "%s/%s" % (self.toc_dir, toc_file)

    def is_makeable(self):
        if not self.collection.is_live():
            self.logger.info("TOC not makeable; collection not set to 'live' (collection: %s)" % (
                self.collection.tag()))
            return False

        html_dir = os.path.join(self.outdir, self.collection.html_dir())
        if not os.path.exists(html_dir):
            self.logger.info("TOC not makeable; no HTML dir found: %s (collection: %s)" % (
                html_dir, self.collection.tag()))
            return False

        html_files = glob.glob(os.path.join(html_dir, '*.html'))
        if len(html_files) == 0:
            self.logger.info("TOC not makeable; no HTML files found in %s (collection %s)" % (
                html_dir, self.collection.tag()))
            return False

        return True

    def is_needed(self):
        if not self.is_makeable():
            return False

        if not os.path.exists(self.outfile_path()):
            return True

        html_dir = os.path.join(self.outdir, self.collection.html_dir())
        html_files = glob.glob(os.path.join(html_dir, '*.html'))
        newest_html = max([os.path.getmtime(x) for x in html_files])
        if os.path.getmtime(self.outfile_path()) > newest_html:
            logging.info("TOC file newer than all HTML files found in %s; skipping %s" % (html_dir, self.collection))
            return False

        return True
