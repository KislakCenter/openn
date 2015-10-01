import os
import logging

from openn.models import *
from openn.openn_db import *
from openn.openn_exception import OPennException

class PrepSetup:
    def prep_document(self, collection, base_dir):
        doc = None
        openn_collection = collection.openn_collection()
        if openn_collection is None:
            msg = "Cannot find collection in database for tag: %s"
            raise OPennException(msg % (collection.tag(),))

        try:
            attrs = {
                'openn_collection': openn_collection,
                'base_dir': base_dir
            }
            doc = Document.objects.get(**attrs)
        except Document.DoesNotExist:
            doc = save_document(attrs)
        return doc
