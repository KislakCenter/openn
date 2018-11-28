# -*- coding: utf-8 -*-
from lxml import etree
from openn.xml.xml_whatsit import XMLWhatsit

class Author(XMLWhatsit):
    def __init__(self, node,ns):
        self.xml = node
        self.ns = ns

    @property
    def name(self):
        if self.has_node('./t:persName'):
            return self._get_text('./t:persName[1]')
        elif self.has_node('./t:name'):
            return self._get_text('./t:name[1]')
        else:
            return self._get_text('.')

    @property
    def ref(self):
        return self._get_attr('.', 'ref')

    def tostring(self):
        return etree.tostring(self.xml, pretty_print=True)
