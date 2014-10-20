# -*- coding: utf-8 -*-

from django.template import Context, Template
from django.conf import settings
from django.template.loader import get_template

from operator import itemgetter

from openn.models import *
from openn.xml.openn_tei import OPennTEI
from openn.pages.pages import Pages
from openn.pages.document_data import DocumentData

class Browse(Pages):

    def __init__(self,doc_id,**kwargs):
        self._doc_id = doc_id
        self._document = Document.objects.get(id=self._doc_id)
        self._data = DocumentData(self._document)

        updated_kwargs = kwargs.update({'template_name': 'browse_ms.html',
                                        'outfile':self.get_outfile_name()})
        super(Browse,self).__init__(**kwargs)

    def get_context(self):
        # items = Document.objects.filter(collection=self.collection)
        return Context({ 'doc': self.data })

    def get_outfile_name(self):
        html_dir = settings.COLLECTIONS[self.collection]['html_dir']
        return '{0}/{1}_browse.html'.format(html_dir, self.document.base_dir)

    @property
    def collection(self):
        return self.document.collection

    @property
    def data(self):
        return self._data

    @property
    def document(self):
        return self._document
