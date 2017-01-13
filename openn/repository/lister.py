# -*- coding: utf-8 -*-
import logging

from copy import deepcopy

from openn.openn_exception import OPennException
from openn.repository.configs import Configs
from openn.repository.details import Details
from openn.models import *

class Lister(Details):
    logger = logging.getLogger(__name__)

    def list_all(self, sort_by = 'name'):
        """Return a list of all collections; sorted by name.
        """

        return self.details(sort_by)
