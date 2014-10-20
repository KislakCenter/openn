# -*- coding: utf-8 -*-
from lxml import etree


class DocumentPage:
    BLANK = 'blank'

    def __init__(self, image, openn_tei):
        """Arguments are an Image object and optional LXML nodes:
        `ms_item` and `deco_note`; both taken from the Document's
        openn_tei instance.

        """
        self._image      = image
        self._tei        = openn_tei
        self._ms_items   = None
        self._deco_notes = None

    @property
    def image(self):
        return self._image

    @property
    def titles(self):
        return [ item.title for item in self.ms_items ]

    @property
    def n(self):
        return self.image.label

    @property
    def ms_items(self):
        if self._ms_items is None:
            self._ms_items = self._tei.ms_items(self.n)
        return self._ms_items

    @property
    def deco_notes(self):
        if self._deco_notes is None:
            self._deco_notes = self._tei.deco_notes(self.n)
        return self._deco_notes
