# -*- coding: utf-8 -*-
import logging
import re

from copy import deepcopy

from openn.openn_exception import OPennException
from openn.collections.configs import Configs
from openn.openn_functions import *
from openn.models import *

class Details(object):
    logger = logging.getLogger(__name__)

    def __init__(self, configs):
        if not isinstance(configs, Configs):
            msg = "Expected type %r; got %r"
            msg = msg  % (Configs,type(configs))
            raise TypeError(msg)

        self._configs = configs

    def sort_key(self,config, sort_by):
        k = config.get(sort_by, '__none__')
        if isinstance(k,str) or isinstance(k,unicode):
            k = re.sub('^(the|an?) +', '', k)

        return k

    def details(self, sort_by = 'name'):
        """Return details of all collections; sorted by name.

        """
        colls = self.collections()
        # create a list of tuples using the key
        tups = [ (self.sort_key(cfg,sort_by), cfg) for cfg in self.collections() ]
        ordered = sorted(tups, key=lambda x: x[0])

        return [ x[1] for x in ordered ]

    def all_tags(self):
        tags = [ c.tag for c in OPennCollection.objects.all() ]
        tags += [ c['tag'] for c in self._configs._configs if c.get('tag') ]

        return set(tags)

    def get_details(self, tag):
        details = { 'tag': tag }
        # get information from the database
        try:
            coll = OPennCollection.objects.get(tag=tag)
            doc_count = Document.objects.filter(openn_collection_id = coll.pk).count()
            details.update({ 'collection_id': coll.long_id(),
                             'metadata_type': coll.metadata_type,
                             'documents': doc_count})

        except OPennCollection.DoesNotExist:
            details.update({ 'collection_id': None,
                             'metadata_type': None,
                             'NOT_IN_DATABASE': 'NOT_IN_DATABASE',
                             'documents': 0})

        # get information from the settings
        try:
            cfg = self._configs.get_config(tag)
            db_mdtype = details['metadata_type']
            cfg_mdtype = details['metadata_type']
            details.update(cfg)
            if db_mdtype is None:
                pass
            elif db_mdtype.lower() != cfg_mdtype.lower():
                s = "CONFLICT -- database: %s; configuration: %s"
                details['metadata_type'] = s
        except OPennException:
            details['name'] = '__NO_CONFIGURATION_FOUND'

        return details

    def collections(self):
        """Return a comprehensive list all collections in the database and all
        collections with configurations.

        """
        collections = []
        for tag in self.all_tags():
            collections.append(self.get_details(tag))
        return collections

    def find_config(self, tag):
        try:
            return self._configs.get_config(tag)
        except OPennException as oe:
            msg = "Error finding config for tag '%s': %s"
            logger.warn(msg % (tag,oe.exception))
        return { 'tag': tag }
