# -*- coding: utf-8 -*-
from lxml import etree
from lxml import objectify
import xmltodict

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

    def _get_strings_for_nodes(self,xpath):
        """Return a list of all the strings for the matched nodes, excluding
        strings that are in children. See `_node_string(node)` for behavior.
        """
        return [' '.join(self._node_strings(n)) for n in self._get_nodes(xpath) ]

    def _get_dict(self,xpath):
        nodes = self._get_nodes(xpath)
        if len(nodes) == 0:
            return {}
        s = etree.tostring(nodes[0], pretty_print=True, xml_declaration=True,
                           encoding='UTF-8')

        return xmltodict.parse(s)

    def _get_objects(self,xpath):
        objs = []
        for e in self._get_nodes(xpath):
            s = etree.tostring(e, pretty_print=True, xml_declaration=True,
                               encoding='UTF-8')
            objs.append(objectify.fromstring(s))

        return objs

    def _node_strings(self, node):
        """ Return all the strings in the node proper, joined by `sep`. Does not
        return strings from child nodes. For example, for a node `x`:

            <node>
                a
                <child>
                    b
                </child>
                c
            </node>


        Node string will return all strings but 'b':

            self._node_string(x) # => ['a',  'c']
        """
        a = []
        if node.text is not None:
            a.append(node.text)

        for sub in node:
            if sub.tail is not None:
                a.append(sub.tail)

        return a

    @property
    def ns(self):
        return {}
