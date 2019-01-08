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
            return self._get_text('./t:name[not(@type = "vernacular")][1]')
        else:
            return self._get_text('./t:persName[not(@type = "vernacular")][1]')

    @property
    def vernacular(self):
        if self.has_node('./t:name[@type = "vernacular"]'):
            return self._get_text('./t:name[@type = "vernacular"]')
        elif self.has_node('./t:persName[@type = "vernacular"]'):
            return self._get_text('./t:persName[@type = "vernacular"]')

    @property
    def ref(self):
        if self.has_node('./t:name'):
            return self._get_attr('./t:name[not(@type = "vernacular")][1]', 'ref')
        else:
            return self._get_attr('./t:persName[not(@type = "vernacular")][1]', 'ref')

    def tostring(self):
        return etree.tostring(self.xml, pretty_print=True)
