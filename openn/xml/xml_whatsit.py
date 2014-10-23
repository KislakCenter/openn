# -*- coding: utf-8 -*-
from lxml import etree

class XMLWhatsit:
    def _get_nodes(self,xpath):
        return self.xml.xpath(xpath, namespaces=self.ns)

    def to_string(self):
        return etree.tostring(self.xml, pretty_print=True, xml_declaration=True, encoding='UTF-8')

    def _get_attr(self,xpath,attr):
        nodes = self._get_nodes(xpath)
        return nodes[0].get(attr) if len(nodes) > 0 else None

    def _get_text(self,xpath):
        nodes = self._get_nodes(xpath)
        return nodes[0].text if len(nodes) > 0 else None
