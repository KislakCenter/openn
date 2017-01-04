# -*- coding: utf-8 -*-
import logging

from copy import deepcopy

from openn.openn_exception import OPennException
from openn.models import *

class Updater(object):
    logger = logging.getLogger(__name__)

    def __init__(self, project_config_list):
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
        self._configs = deepcopy(project_config_list)

    def update(self,config_dict):
        tag = config_dict['tag']
        project = self.find_or_create_project(config_dict)
        if self.has_changed(project, config_dict) is True:
            for key in config_dict.keys():
                if key != 'tag' and getattr(project, key) != config_dict[key]:
                    setattr(project, key, config_dict[key])
            project.save()
        return project

    def update_all(self):
        for config_dict in self._configs:
            self.update(config_dict)

    def find_or_create_project(self, config_dict):
        # confirm that the tag is valid
        attrs = { 'tag': config_dict['tag'] }
        try:
            project = Project.objects.get(**attrs)
            self.logger.info("Project already exists: '%s'" % (project.tag,))
        except Project.DoesNotExist:
            project = Project(**config_dict)
            self.logger.info("Creating collection: %s" % (project.tag,))
            project.save()

        return project

    def has_changed(self, current_project, config_dict):
        for key in config_dict.keys():
            if key == 'tag':
                continue
            new_val = config_dict[key]
            curr_val = getattr(current_project, key)
            if new_val != curr_val:
                return True
        return False
