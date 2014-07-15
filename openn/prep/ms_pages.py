from django.template import Context, Template, loader
from django.conf import settings
from openn.models import *

class MSPages(object):
    def browse_page(self, doc_id):
        doc = Document.objects.get(id=doc_id)
        c = Context({ 'doc': doc })
        t = loader.get_template('browse_ms.html')
        return t.render(c)


