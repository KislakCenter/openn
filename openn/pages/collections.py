# -*- coding: utf-8 -*-

from django.template import Context, Template
from django.conf import settings
from django.template.loader import get_template

from operator import itemgetter

from openn.pages.pages import Pages

class Collections(Pages):

    def get_context(self):
        collections = [ settings.COLLECTIONS[x] for x in settings.COLLECTIONS ]
        collections.sort(key=itemgetter('name'))
        return Context({ 'collections': collections })
