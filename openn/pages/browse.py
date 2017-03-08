# -*- coding: utf-8 -*-

import logging
from datetime import datetime

from django.template import Context, Template
from django.template.loader import get_template

from operator import itemgetter

from openn.models import *
from openn.xml.openn_tei import OPennTEI
from openn.pages.page import Page
from openn.pages.document_data import DocumentData
import openn.openn_functions as opfunc

class Browse(Page):

    human_name = "Browse"

    logger = logging.getLogger(__name__)

    def __init__(self,document, repository_wrapper, toc_dir,**kwargs):
        self._data = DocumentData(document, repository_wrapper, toc_dir)

        updated_kwargs = kwargs.update({'template_name': 'browse_ms.html',
                                        'outfile': self.document.browse_path})
        super(Browse,self).__init__(**kwargs)
        self.add_after_write('update_hashes')

    def get_context(self,ctx_dict={}):
        ctx = { 'doc': self.data }
        ctx.update(ctx_dict)
        return super(Browse, self).get_context(ctx)

    @property
    def data(self):
        return self._data

    @property
    def title(self):
        return "%s %s" % (self.document.call_number, self.document.title)

    @property
    def document(self):
        return self._data.document

    def log_msg(self, msg_type, msg):
        msg = "%s; %s: %s/%s" % (
            msg_type, msg, self.document.repository.tag, self.document.base_dir)
        self.logger.info(msg)


    def is_makeable(self):
        if not self.document.is_online:
            self.log_msg("page not makeable", "document not online")
            return False

        if not (self.document.tei_xml and len(self.document.tei_xml) > 0):
            self.log_msg("page not makeable", "document lacks TEI")
            return False

        return True

    def is_needed(self, strict=True):
        if not self.is_makeable() and strict is True:
            return False

        if not self.document.prepstatus.succeeded:
            self.log_msg("page not needed", "document's last prep failed")
            return False

        # needed if it doesn't exist
        if not self.output_file_exists():
            return True

        # needed if template has changed
        if self.template_changed():
            return True

        if not self.changed_since_generation(comp_date=self.document.prepstatus.started):
            return False

        return True
