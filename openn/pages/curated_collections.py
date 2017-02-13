# -*- coding: utf-8 -*-
import logging
import os

from django.template import Context, Template
from django.template.loader import get_template

from operator import itemgetter

from openn.models import CuratedCollection
from openn.curated.membership_manager import MembershipManager
from openn.pages.page import Page

class CuratedCollections(Page):

    logger = logging.getLogger(__name__)

    def __init__(self, template_name, outdir, **kwargs):
        self._live_collections = None
        super(CuratedCollections, self).__init__(template_name, outdir, **kwargs)

    def get_context(self, ctx_dict={}):
        collections = self.live_curated_colls()

        collections.sort(key=lambda x: x.name)
        ctx = {'curated_collections': collections}
        ctx.update(ctx_dict)
        return super(CuratedCollections, self).get_context(ctx)

    @property
    def title(self):
        return 'Curated Collections'

    def live_curated_colls(self):
        """ Extract live curated collections """

        if self._live_collections is None:
            self._live_collections = MembershipManager.active_collections()


        return self._live_collections

    def live_curated_colls_count(self):
        return len(self.live_curated_colls())

    def is_needed(self):
        """If the curated collections template exits, we always say it's needed.

        Why? If implemented, the tests for creating an updated curated
        collections list page would ask the following.  A Yes answer to any
        would trigger page generation.

        1. Is there no existing CuratedCollections.html file?

        2. Is the template newer than the current CuratedCollections.html
           file?

        3. Has the collection information for any of the live collections in
           the database changed?

        4. Are there now 'live' curated collections with live documents which
           did not appear in the previous curated collections list?

        The file is small and cheap to build; #2 will almost never happen; and
        nos. 3 & 4 are too complicated to be worth figuring out.

        Therefore, we always say the page is needed if it's makeable.

        """
        return self.is_makeable()

    def is_makeable(self):
        """ Page is makeable if there are live curate collections with
        documents.
        """
        return self.live_curated_colls_count() > 0
