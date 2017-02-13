# -*- coding: utf-8 -*-

import logging

from django.template import Context, Template
from django.template.loader import get_template

from operator import itemgetter
from datetime import datetime

from openn.models import *
import openn.openn_functions as opfunc
from openn.pages.page import Page
from openn.pages.document_data import DocumentData

class CuratedCollectionTOC(Page):

    logger = logging.getLogger(__name__)

    def __init__(self, curated_tag, toc_dir, **kwargs):
        self.curated_collection = CuratedCollection.objects.get(tag=unicode(curated_tag))
        self.toc_dir = toc_dir
        kwargs.update({'outfile':self.toc_path()})
        super(CuratedCollectionTOC,self).__init__(**kwargs)

    def toc_path(self):
        return "%s/%s" % (self.toc_dir, self.curated_collection.toc_file())

    def get_context(self,ctx_dict={}):
        # docs  = self.curated_collection.documents.filter(is_online=True).order_by('repository__name', 'call_number')
        # items = [ DocumentData(x, self.curated_collection, self.toc_dir) for x in docs ]
        items = self.build_docs()
        ctx   = { 'curated_collection': self.curated_collection, 'items_by_repository': items }
        ctx.update(ctx_dict={})
        return super(CuratedCollectionTOC, self).get_context(ctx)

    def is_makeable(self):
        if not self.curated_collection.live:
            self.logger.info("Curated collection HTML TOC not makeable; curated collection not set to 'live' (curated collection: %s)" % (
                self.curated_collection.tag()))
            return False

        if self.curated_collection.csv_only:
            self.logger.info("Curated collection HTML TOC not makeable; "
                             "curated collection is CSV-only  (curated collection: %s",
                             self.curated_collection.tag)
            return False

        if self.curated_collection.documents.count() == 0:
            self.logger.info("Curated collection HTML TOC not makeable; curated collection has no documents: %s" % (self.curated_collection.tag,))
            return False

        doc_count = self.curated_collection.documents.filter(is_online=True).count()
        if doc_count == 0:
            self.logger.info("Curated collection HTML TOC not makeable; curated collection has no documents online: %s" % (self.curated_collection.tag,))
            return False

        return True

    def is_needed(self):
        if not self.is_makeable():
            return False

        # needed if it doesn't exist
        if not os.path.exists(self.outfile_path()):
            return True

        # see if it's out-of-date
        latest_doc = self.curated_collection.documents.filter(is_online=True).latest('updated')

        current_file_date = opfunc.mtime_to_datetime(self.outfile_path())
        if current_file_date > latest_doc.updated:
            logging.info("Curated collection HTML TOC up-to-date; skipping %s",
                         self.curated_collection.tag,)
            return False

        return True

    def get_repositories(self):
        repo_ids = self.curated_collection.documents.filter(is_online=True).order_by('repository').values_list('repository', flat=True).distinct()
        print "repo_ids are %s" % (str(repo_ids,))
        repos    = [ Repository.objects.get(pk=x) for x in repo_ids ]
        repos.sort(key=lambda x: x.name)

        return repos

    def build_docs(self):
        groups = []
        for repo in self.get_repositories():
            group          = { 'repository': repo }
            docs           = self.curated_collection.documents.filter(is_online=True, repository=repo)
            group['items'] = [ DocumentData(x, self.curated_collection, self.toc_dir) for x in docs ]
            groups.append(group)

        return groups

