# -*- coding: utf-8 -*-

from django.template import Context, Template
from django.conf import settings
from django.template.loader import get_template

from operator import itemgetter

from openn.pages.page import Page

class Collections(Page):

    def get_context(self):
        collections = [ settings.COLLECTIONS[x] for x in settings.COLLECTIONS ]
        collections.sort(key=itemgetter('name'))
        return Context({ 'collections': collections })

    def is_needed(self):
        """If the collections template exits; we always say it's needed.

        Why? If implemented, the tests for creating a new collections list
        page would ask the following.  A Yes answer to any would trigger
        page generation.

        1. Is there no existing 3_Collections.html file?

        2. Is the template newer than the current 3_Collections.html file?

        3. Has the collection information in the settings file changed?

        4. Are there new TOC files for collections not listed in the
           current 3_Collections.html?

        Nos. 3 and 4 are too complicated to make it worth figuring out.

        Therefore, we always say the page is needed.

        """
        return self.is_makeable()
