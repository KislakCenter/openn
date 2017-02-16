# -*- coding: utf-8 -*-

from django.conf import settings

from openn.models import *
from openn.xml.openn_tei import OPennTEI
from openn.pages.document_page import DocumentPage

class DocumentData:
    def __init__(self, document, repository, toc_dir):
        self._document      = document
        self._repository    = repository
        self._toc_dir       = toc_dir
        self._tei           = OPennTEI(document.tei_xml)
        self._pages         = None
        self._ms_item_pages = None
        self._deco_notes    = None

    @property
    def tei(self):
        return self._tei

    @property
    def document(self):
        return self._document

    @property
    def repository(self):
        return self._repository

    @property
    def toc_path(self):
        toc_file = self._repository.toc_file()
        return "/%s/%s" % (self._toc_dir, toc_file)

    @property
    def pages(self):
        if self._pages is None:
            self._pages = []
            for image in self._document.image_set.all():
                self._pages.append(DocumentPage(image,self.tei))
        return self._pages

    @property
    def document_location(self):
        parts = [self.tei.settlement, self.tei.institution, self.tei.repository]
        parts = [ x for x in parts if x is not None ]
        return ', '.join(parts)

    @property
    def ms_item_pages(self):
        if self._ms_item_pages is None:
            self._ms_item_pages = [ p for p in self.pages if len(p.ms_items) > 0 ]
        return self._ms_item_pages

    @property
    def deco_note_pages(self):
        if self._deco_notes is None:
            self._deco_notes = [ p for p in self.pages if len(p.deco_notes) > 0 ]
        return self._deco_notes

    def has_toc(self):
        return len(self.ms_item_pages) > 0

    def has_deco_list(self):
        return len(self.deco_note_pages) > 0

    def origin(self):
        return [x for x in [ self.tei.orig_place, self.tei.orig_date ] if x ]
