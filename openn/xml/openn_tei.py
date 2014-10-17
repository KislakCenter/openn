from lxml import etree
from StringIO import StringIO
import re

from openn.xml.xml_whatsit import XMLWhatsit
from openn.xml.ms_item import MSItem

class OPennTEI(XMLWhatsit):
    TEI_NS = 'http://www.tei-c.org/ns/1.0'
    fix_path_re = re.compile('^data/')

    def __init__(self, xml):
        if isinstance(xml, str):
            parser = etree.XMLParser(recover=True, encoding='utf-8')
            self.xml = etree.fromstring(xml, parser)
        elif isinstance(xml, unicode):
            parser = etree.XMLParser(recover=True, encoding='utf-8')
            # self.xml = etree.parse(StringIO(xml.encode('utf-8')), parser)
            self.xml = etree.parse(StringIO(xml.encode('utf-8')), parser)
        else:
            parser = etree.XMLParser(remove_blank_text=True)
            self.xml = etree.parse(xml, parser)
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

    @property
    def settlement(self):
        return self._get_text('//t:msIdentifier/t:settlement')

    @property
    def institution(self):
        return self._get_text('//t:msIdentifier/t:institution')

    @property
    def repository(self):
        return self._get_text('//t:msIdentifier/t:repository')

    @property
    def summary(self):
        return self._get_text('//t:msContents/t:summary')

    @property
    def license(self):
        return self._get_text('//t:publicationStmt/t:availability/t:licence')

    @property
    def license_url(self):
        return self._get_attr('//t:publicationStmt/t:availability/t:licence', 'target')

    @property
    def publisher(self):
        return self._get_text('//t:publicationStmt/t:publisher')

    @property
    def text_lang(self):
        return self._get_text('//t:msContents/t:textLang')

    @property
    def orig_date(self):
        return self._get_text('//t:history/t:origin/t:origDate')

    @property
    def orig_place(self):
        return self._get_text('//t:history/t:origin/t:origPlace')

    @property
    def ms_items(self):
        return  [MSItem(node,self.ns) for node in self._get_nodes('//t:msContents/t:msItem')]

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
        facs = self.xml.xpath(xpath, namespaces=self.ns)[0]
        for fdata in file_list.document_files:
            surface = etree.Element("surface", n=fdata.label, nsmap=self.ns)
            for dtype in fdata.derivs:
                deriv = fdata.get_deriv(dtype)
                path = OPennTEI.fix_path_re.sub("", deriv['path'])
                attrs = {}
                attrs['url'] = path
                attrs['width'] = "%spx" % str(deriv['width'])
                attrs['height'] = "%spx" % str(deriv['height'])
                graphic = etree.Element('graphic', **attrs)
                surface.append(graphic)
            facs.append(surface)
