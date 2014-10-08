# -*- coding: utf-8 -*-

from django.template import Context, Template
from django.conf import settings
from django.template.loader import get_template

from operator import itemgetter

from openn.models import *
from openn.pages.pages import Pages

class Browse(Pages):

    def __init__(self, doc_id,collection,**kwargs):
        self.collection = collection
        self.doc_id = doc_id
        updated_kwargs = kwargs.update({'template_name': 'browse_ms.html',
                                        'outfile':self.get_outfile_name()})
        super(Browse,self).__init__(**kwargs)

    def get_context(self):
        # items = Document.objects.filter(collection=self.collection)
        doc = self.document()
        return Context({ 'doc': doc })

    def get_outfile_name(self):
        html_dir = settings.COLLECTIONS[self.collection]['html_dir']
        return '{0}/{1}_browse.html'.format(html_dir, self.document().base_dir)

    def document(self):
        return Document.objects.get(id=self.doc_id)
