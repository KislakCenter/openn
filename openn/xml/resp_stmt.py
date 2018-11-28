# -*- coding: utf-8 -*-
from lxml import etree
from openn.xml.xml_whatsit import XMLWhatsit

class RespStmt(XMLWhatsit):
    def __init__(self, node,ns):
        self.xml = node
        self.ns = ns

    @property
    def resp(self):
        return self._get_text('./t:resp')

    @property
    def name(self):
        if self.has_node('./t:name'):
            return self._get_text('./t:name[1]')
        else:
            return self._get_text('./t:persName[1]')

    @property
    def ref(self):
        if self.has_node('./t:name'):
            return self._get_attr('./t:name[1]', 'ref')
        else:
            return self._get_attr('./t:persName[1]', 'ref')

    def tostring(self):
        return etree.tostring(self.xml, pretty_print=True)
