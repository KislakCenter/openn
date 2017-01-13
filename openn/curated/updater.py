# -*- coding: utf-8 -*-
import logging

from copy import deepcopy

from openn.openn_exception import OPennException
from openn.models import *

class Updater(object):
    logger = logging.getLogger(__name__)

    def __init__(self, curated_config_list):
        """Instantiate a new Update with a list of config dicts. Dicts should be
        formatted as below.

                {
                    'tag': '        bibliophilly',
                    'name':         'Bibliotheca Philadelphiensis',
                    'blurb':        'Lorem ipsum...',
                    'csv_only':     False,
                    'include_file': 'BiblioPhilly.html',
                    'live':         True,
                },
        """
        self._configs = deepcopy(curated_config_list)

    def update(self,config_dict):
        tag = config_dict['tag']
        curated = self.find_or_create_curated_collection(config_dict)
        if self.has_changed(curated, config_dict) is True:
            for key in config_dict.keys():
                if key != 'tag' and getattr(curated, key) != config_dict[key]:
                    setattr(curated, key, config_dict[key])
            curated.save()
        return curated

    def update_all(self):
        for config_dict in self._configs:
            self.update(config_dict)

    def find_or_create_curated_collection(self, config_dict):
        # confirm that the tag is valid
        attrs = { 'tag': config_dict['tag'] }
        try:
            curated = CuratedCollection.objects.get(**attrs)
            self.logger.info("CuratedCollection already exists: '%s'" % (curated.tag,))
        except CuratedCollection.DoesNotExist:
            curated = CuratedCollection(**config_dict)
            self.logger.info("Creating curated: %s" % (curated.tag,))
            curated.save()

        return curated

    def has_changed(self, current_curated, config_dict):
        for key in config_dict.keys():
            if key == 'tag':
                continue
            new_val = config_dict[key]
            curr_val = getattr(current_curated, key)
            if new_val != curr_val:
                return True
        return False
