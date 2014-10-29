# -*- coding: utf-8 -*-
from lxml import etree
from StringIO import StringIO
import re

from openn.xml.xml_whatsit import XMLWhatsit
from openn.xml.ms_item import MSItem
from openn.xml.licence import Licence
from openn.xml.resp_stmt import RespStmt

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
    def licences(self):
        if not getattr(self, '_licences', None):
            xpath = '//t:publicationStmt/t:availability/t:licence'
            self._licences = [Licence(n, self.ns) for n in self._get_nodes(xpath)]
        return self._licences

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
        if not getattr(self, '_ms_items', None):
            xpath = '//t:msContents/t:msItem'
            self._ms_items = [MSItem(node,self.ns) for node in self._get_nodes(xpath)]
        return self._ms_items

    @property
    def notes(self):
        if not getattr(self, '_notes'):
            xpath = '//t:notesStmt/t:notes'
            self._notes = self._all_the_strings(xpath)
        return self._notes

    @property
    def genres(self):
        if not getattr(self, '_genres', None):
            xpath = '//t:keywords[@n="form/genre"]/t:term'
            self._genres = self._all_the_strings(xpath)
        return self._genres

    @property
    def subjects(self):
        if not getattr(self, '_subjects', None):
            xpath = '//t:keywords[@n="subjects"]/t:term'
            self._subjects = self._all_the_strings(xpath)
        return self._subjects

    @property
    def support(self):
        return self._get_text('//t:supportDesc/t:support')

    @property
    def extent(self):
        return self._get_text('//t:supportDesc/t:extent')

    @property
    def provenance(self):
        if not getattr(self, '_provenance', None):
            xpath = '//t:history/t:provenance'
            self._provenance = self._all_the_strings(xpath)
        return self._provenance

    @property
    def authors(self):
        if not getattr(self, '_authors', None):
            xpath = '//t:msContents/t:msItem[1]/t:author'
            self._authors = self._all_the_strings(xpath)
        return self._authors

    def related_names(self):
        if not getattr(self, '_related_names', None):
            self._related_names = [RespStmt(n,self.ns) for n in self._get_nodes('//t:msContents/t:msItem[1]/t:respStmt')]
        return self._related_names

    def ms_items(self, n):
        nodes = self._get_nodes('//t:msItem[@n="%s"]' % n)
        return [ MSItem(node, self.ns) for node in nodes ]

    def deco_notes(self, n):
        nodes = self._get_nodes('//t:decoNote[@n="%s"]' % n)
        return [node.text for node in nodes ]

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
        # clear the facs
        for graphic in self.xml.xpath('/t:TEI/t:facsimile/t:graphic', namespaces=self.ns):
            graphic.getparent().remove(graphic)
        # add the surface/graphic elements
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
