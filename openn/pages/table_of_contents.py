# -*- coding: utf-8 -*-

import glob
import logging

from django.template import Context, Template
from django.conf import settings
from django.template.loader import get_template

from operator import itemgetter

from openn.models import *
from openn.pages.page import Page
from openn.pages.document_data import DocumentData

class TableOfContents(Page):

    logger = logging.getLogger(__name__)

    def __init__(self, collection,**kwargs):
        self.collection = collection
        updated_kwargs = kwargs.update({'outfile':self.toc_path()})
        super(TableOfContents,self).__init__(**kwargs)


    def get_context(self,ctx_dict={}):
        docs = Document.objects.filter(
            collection=self.collection, is_online=True)
        items = [ DocumentData(x) for x in docs ]
        ctx = { 'collection': settings.COLLECTIONS[self.collection],
                'items': items }
        ctx.update(ctx_dict={})
        return super(TableOfContents, self).get_context(ctx)

    @property
    def collection_config(self):
        return settings.COLLECTIONS[self.collection]

    @property
    def title(self):
        return self.collection_config['name']

    def toc_path(self):
        toc_file = self.collection_config['toc_file']
        return "%s/%s" % (settings.TOC_DIR, toc_file)


    def is_makeable(self):
        if not self.collection_is_live():
            self.logger.info("TOC not makeable; collection not set to 'live' (collection: %s)" % (
                self.collection))
            return False

        html_dir = os.path.join(self.outdir, self.collection_config['html_dir'])
        if not os.path.exists(html_dir):
            self.logger.info("TOC not makeable; no HTML dir found: %s (collection: %s)" % (
                html_dir, self.collection))
            return False

        html_files = glob.glob(os.path.join(html_dir, '*.html'))
        if len(html_files) == 0:
            self.logger.info("TOC not makeable; no HTML files found in %s (collection %s)" % (
                html_dir, self.collection))
            return False

        return True

    def collection_is_live(self):
        coll_dict = settings.COLLECTIONS[self.collection]
        return coll_dict.get('live', False)

    def is_needed(self):
        if not self.is_makeable():
            return False

        if not os.path.exists(self.outfile_path()):
            return True

        html_dir = os.path.join(self.outdir, self.collection_config['html_dir'])
        html_files = glob.glob(os.path.join(html_dir, '*.html'))
        newest_html = max([os.path.getmtime(x) for x in html_files])
        if os.path.getmtime(self.outfile_path()) > newest_html:
            logging.info("TOC file newer than all HTML files found in %s; skipping %s" % (html_dir, self.collection))
            return False

        return True
