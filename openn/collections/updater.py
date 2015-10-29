# -*- coding: utf-8 -*-
import logging

from copy import deepcopy

from openn.openn_exception import OPennException
from openn.models import *

class Updater(object):
    logger = logging.getLogger(__name__)

    def __init__(self, collection_configs):
        self._configs = collection_configs

    def update(self,tag):
        self.find_or_create_collection(tag)

    def update_all(self):
        for cfg in settings.COLLECTIONS['configs']:
            tag  = cfg['tag']
            self.update(tag)

    def find_or_create_collection(self, tag):
        # confirm that the tag is valid
        self._configs.get_config(tag)
        attrs = { 'tag': tag }
        try:
            coll = OPennCollection.objects.get(**attrs)
            self.logger.info("Collection already exists: '%s'" % (coll.tag,))
        except OPennCollection.DoesNotExist:
            coll = OPennCollection(tag = tag)
            self.logger.info("Creating collection: %s" % (coll.tag,))
            coll.save()

        return coll
