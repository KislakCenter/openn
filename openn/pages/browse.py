# -*- coding: utf-8 -*-

from django.template import Context, Template
from django.conf import settings
from django.template.loader import get_template

from operator import itemgetter

from openn.models import *
from openn.xml.openn_tei import OPennTEI
from openn.pages.page import Page
from openn.pages.document_data import DocumentData

class Browse(Page):

    def __init__(self,doc_id,**kwargs):
        self._doc_id = doc_id
        self._document = Document.objects.get(id=self._doc_id)
        self._data = DocumentData(self.document)

        updated_kwargs = kwargs.update({'template_name': 'browse_ms.html',
                                        'outfile':self.document.browse_path})
        super(Browse,self).__init__(**kwargs)

    def get_context(self):
        # items = Document.objects.filter(collection=self.collection)
        return Context({ 'doc': self.data })

    @property
    def data(self):
        return self._data

    @property
    def document(self):
        return self._document
