# -*- coding: utf-8 -*-
import logging

from copy import deepcopy

from openn.openn_exception import OPennException
from openn.models import *

class Updater(object):
    logger = logging.getLogger(__name__)

    def __init__(self, repository_configs):
        self._configs = repository_configs


    def update(self, tag, config_dict):
        repo = self.find_or_create_repository(tag)
        if self.has_changed(repo, config_dict):
            self.logger.info("Updating repository: %s" % (repo.tag,))
            for key in config_dict.keys():
                if key == 'tag':
                    continue
                new_val = config_dict[key]
                if getattr(repo,key) == new_val:
                    continue
                self.logger.info("Updating repository '%s' field '%s' to '%s'" % (repo.tag, key, unicode(new_val).encode('utf8')))
                setattr(repo, key, new_val)
                repo.save()

        return repo

    def update_all(self):
        for config_dict in settings.REPOSITORIES['configs']:
            tag  = config_dict['tag']
            self.update(tag, config_dict)

    def find_or_create_repository(self, tag):
        # confirm that the tag is valid
        attrs = { 'tag': tag }
        try:
            repo = Repository.objects.get(**attrs)
            self.logger.info("Repository already exists: '%s'" % (repo.tag,))
        except Repository.DoesNotExist:
            attrs = self._configs.get_config_dict(tag)
            repo = Repository(**attrs)
            self.logger.info("Creating repository: %s" % (repo.tag,))
            repo.save()

        return repo

    def has_changed(self, current_repo, config_dict):
        for key in config_dict.keys():
            if key == 'tag':
                continue
            new_val = config_dict[key]
            curr_val = getattr(current_repo, key)
            if new_val != curr_val:
                return True
        return False