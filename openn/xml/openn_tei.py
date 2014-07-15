from lxml import etree
import re

class OPennTEI:
    TEI_NS = 'http://www.tei-c.org/ns/1.0'
    fix_path_re = re.compile('^data/')

    def __init__(self, tei_path, mode='r'):
        parser = etree.XMLParser(remove_blank_text=True)
        self.tei = etree.parse(open(tei_path, mode), parser)
        self._namespaces = { 't': OPennTEI.TEI_NS }

    @property
    def ns(self):
        return self._namespaces

    @property
    def call_number(self):
        return self._get_text('//t:msIdentifier/t:idno')

    @property
    def title(self):
        return self._get_text('//t:msContents/t:msItem/t:title')

    def add_file_list(self,file_list):
        """
           <facsimile>
              <surface n="Front cover">
                 <graphic url="ljs041_wk1_front0001.tif"/>
              </surface>
              <surface n="Inside front cover">
                 <graphic url="ljs041_wk1_front0002.tif"/>
              </surface>
              ...
           </facsimile>
        """
        xpath = '/t:TEI/t:facsimile'
        facs = self.tei.xpath(xpath, namespaces=self.ns)[0]
        for fdata in file_list.document_files:
            surface = etree.Element("surface", n=fdata.label, nsmap=self.ns)
            for dtype in fdata.derivs:
                deriv = fdata.get_deriv(dtype)
                path = OPennTEI.fix_path_re.sub("", deriv['path'])
                attrs = {}
                attrs['url'] = path
                attrs['width'] = str(deriv['width'])
                attrs['height'] = str(deriv['height'])
                graphic = etree.Element('graphic', **attrs)
                surface.append(graphic)
            facs.append(surface)
        # print etree.tostring(facs,pretty_print=True)

    def to_string(self):
        print etree.tostring(self.tei, pretty_print=True, xml_declaration=True, encoding='UTF-8')

    def _get_text(self,xpath):
        nodes = self._get_nodes(xpath)
        return nodes[0].text if len(nodes) > 0 else None

    def _get_nodes(self,xpath):
        return self.tei.xpath(xpath, namespaces=self.ns)
