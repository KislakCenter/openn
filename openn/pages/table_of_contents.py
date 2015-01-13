# -*- coding: utf-8 -*-

from django.template import Context, Template
from django.conf import settings
from django.template.loader import get_template

from operator import itemgetter

from openn.models import *
from openn.pages.page import Page
from openn.pages.document_data import DocumentData

class TableOfContents(Page):

    def __init__(self, collection,**kwargs):
        self.collection = collection
        updated_kwargs = kwargs.update({'outfile':self.get_toc_file_name()})
        super(TableOfContents,self).__init__(**kwargs)

    def get_context(self):
        docs = Document.objects.filter(collection=self.collection, is_online=True)
        items = [ DocumentData(x) for x in docs ]
        return Context({ 'collection': settings.COLLECTIONS[self.collection],
                         'items': items })

    def get_toc_file_name(self):
        return settings.COLLECTIONS[self.collection]['toc_file']
