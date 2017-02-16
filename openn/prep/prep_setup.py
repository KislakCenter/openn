import os
import logging

from openn.models import *
from openn.openn_db import *
from openn.openn_exception import OPennException

class PrepSetup:
    def prep_document(self, repo_wrapper, base_dir):
        doc = None
        repository = repo_wrapper.repository()
        if repository is None:
            msg = "Cannot find repo_wrapper in database for tag: %s"
            raise OPennException(msg % (repo_wrapper.tag(),))

        try:
            attrs = {
                'repository': repository,
                'base_dir': base_dir
            }
            doc = Document.objects.get(**attrs)
        except Document.DoesNotExist:
            doc = save_document(attrs)
        return doc
