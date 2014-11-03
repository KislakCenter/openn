# -*- coding: utf-8 -*-
from datetime import date
from openn.xml.openn_tei import OPennTEI
from openn.md.dublin_core import DublinCore

class CommonDC(DublinCore):
    def __init__(self, document):
        self._document = document
        self._tei = OPennTEI(self.document.tei_xml)

    @property
    def document(self):
        return self._document

    @property
    def tei(self):
        return self._tei

    def dc_relation(self):
        return [ n.text for n in self.tei.alt_identifiers ]

    def dc_subject(self):
        return self.tei.subjects + self.tei.genres

    def dc_publisher(self):
        return self.tei.publisher

    def dc_creator(self):
        """ Return the authors of the TEI file or its publisher.
        """
        if len(self.tei.tei_authors) > 0:
            return self.tei.tei_authors
        else:
            return self.tei.publisher
