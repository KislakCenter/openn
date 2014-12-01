import os
import logging

from openn.models import *
from openn.openn_db import *

class PrepSetup:
    def prep_document(self, collection, base_dir):
        doc = None
        try:
            attrs = {
                'collection': collection,
                'base_dir': base_dir
            }
            doc = Document.objects.get(**attrs)
        except Document.DoesNotExist:
            doc = save_document(attrs)
        return doc
