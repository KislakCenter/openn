# -*- coding: utf-8 -*-
import logging
import os

from django.template import Context, Template
from django.template.loader import get_template

from operator import itemgetter

from openn.pages.page import Page

class Collections(Page):

    logger = logging.getLogger(__name__)

    def __init__(self, template_name, outdir, coll_configs,**kwargs):
        self._coll_configs = coll_configs
        super(Collections,self).__init__(template_name, outdir, **kwargs)

    def get_context(self, ctx_dict={}):
        collections = self.live_collections()

        collections.sort(key=lambda x: x.name())
        ctx = { 'collections': collections }
        ctx.update(ctx_dict)
        return super(Collections, self).get_context(ctx)

    @property
    def title(self):
        return 'Collections'

    def live_collections(self, ):
        live_ones = []

        for coll in self._coll_configs.all_collections():
            if coll.is_live():
                html_dir = os.path.join(self.outdir, coll.html_dir())
                if os.path.exists(html_dir):
                    msg = "Collection added to collections page (%s)"
                    msg += " (collection is live and has 'html' dir: %s)"
                    msg = msg % (coll.tag(), html_dir)
                    live_ones.append(coll)
                elif coll.no_document():
                    # if this is a no-document collection, add it
                    msg = "Collection added to collections page (%s)"
                    msg += " (collection is live and is marked no_document)"
                    msg = msg % (coll.tag())
                    live_ones.append(coll)
                else:
                    msg = "Collection not added to collections page (%s);"
                    msg += " collection set to 'live',"
                    msg += " but HTML directory does not exist: '%s'"
                    msg = msg % (coll.tag(), html_dir,)
            else:
                msg = "Collection not added to collections page (%s);"
                msg += " collection not set to 'live'"
                msg = msg % (coll.tag(),)
            self.logger.info(msg)

        return live_ones

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
