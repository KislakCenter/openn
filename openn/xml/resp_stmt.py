# -*- coding: utf-8 -*-
from lxml import etree
from openn.xml.xml_whatsit import XMLWhatsit

class RespStmt(XMLWhatsit):
    def __init__(self, node,ns):
        self.xml = node
        self.ns = ns

    @property
    def resp(self):
        return self._get_text('.//t:resp')

    @property
    def pers_name(self):
        return self._get_text('.//t:persName')

    def tostring(self):
        return etree.tostring(self.xml, pretty_print=True)
