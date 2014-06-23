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
        xpath = '//t:msIdentifier/t:idno'
        return self.tei.xpath(xpath, namespaces=self.ns)[0].text

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
                path = OPennTEI.fix_path_re.sub("", fdata.get_deriv_path(dtype))
                graphic = etree.Element('graphic', url=path)
                surface.append(graphic)
            facs.append(surface)
        # print etree.tostring(facs,pretty_print=True)

    def to_string(self):
        print etree.tostring(self.tei, pretty_print=True, xml_declaration=True, encoding='UTF-8')
