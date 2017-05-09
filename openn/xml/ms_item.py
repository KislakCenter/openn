# -*- coding: utf-8 -*-
from lxml import etree
from openn.xml.xml_whatsit import XMLWhatsit

class MSItem(XMLWhatsit):
    def __init__(self, node,ns):
        self.xml = node
        self.ns = ns

    @property
    def title(self):
        return self._get_text('.//t:title')

    @property
    def incipit(self):
        return self._get_text('.//t:incipit')

    @property
    def explicit(self):
        return self._get_text('.//t:explicit')

    @property
    def locus(self):
        return self._get_text('.//t:locus')

    def tostring(self):
        return etree.tostring(self.xml, pretty_print=True)
