# -*- coding: utf-8 -*-
import logging

from copy import deepcopy

from openn.openn_exception import OPennException
from openn.models import *

class Updater(object):
    logger = logging.getLogger(__name__)

    def __init__(self, repository_configs):
        self._configs = repository_configs

    def update(self,tag):
        self.find_or_create_repository(tag)

    def update_all(self):
        for cfg in settings.REPOSITORIES['configs']:
            tag  = cfg['tag']
            self.update(tag)

    def find_or_create_repository(self, tag):
        # confirm that the tag is valid
        cfg = self._configs.get_config(tag)
        attrs = { 'tag': tag }
        try:
            repo = Repository.objects.get(**attrs)
            self.logger.info("Repository already exists: '%s'" % (repo.tag,))
        except Repository.DoesNotExist:
            metadata_type = cfg['metadata_type']
            repo = Repository(tag = tag, metadata_type = metadata_type)
            self.logger.info("Creating repository: %s" % (repo.tag,))
            repo.save()

        return repo
