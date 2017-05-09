# -*- coding: utf-8 -*-
from lxml import etree
from openn.xml.xml_whatsit import XMLWhatsit

class RelatedResource(XMLWhatsit):
    def __init__(self, node,ns):
        self.xml = node
        self.ns = ns

    @property
    def text(self):
        return self._get_text('.')

    @property
    def target(self):
        return self._get_attr('.', 'target')

    def tostring(self):
        return etree.tostring(self.xml, pretty_print=True)
