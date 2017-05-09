# -*- coding: utf-8 -*-
from lxml import etree
from openn.xml.xml_whatsit import XMLWhatsit

class Author(XMLWhatsit):
    def __init__(self, node,ns):
        self.xml = node
        self.ns = ns

    @property
    def name(self):
        return self._get_text('.')

    @property
    def ref(self):
        return self._get_attr('.', 'ref')

    def tostring(self):
        return etree.tostring(self.xml, pretty_print=True)
