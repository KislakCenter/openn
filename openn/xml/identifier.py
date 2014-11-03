# -*- coding: utf-8 -*-
from lxml import etree
from openn.xml.xml_whatsit import XMLWhatsit

class Identifier(XMLWhatsit):
    def __init__(self,node,ns):
        self.xml = node
        self.ns = ns

    def is_url(self,t):
        return t.strip().startswith('http')

    @property
    def id_type(self):
        return self._get_attr('.', 'type')

    @property
    def text(self):
        t = self._get_text('./t:idno')
        if self.is_url(t):
            return t
        elif self.element_name() == 'msIdentifier':
            return t
        else:
            return "%s: %s" % (self.id_type, t)

    def element_name(self):
        return self.xml.xpath('name(.)')

    def tostring(self):
        return etree.tostring(self.xml, pretty_print=True)
