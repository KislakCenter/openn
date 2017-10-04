# -*- coding: utf-8 -*-
from lxml import etree
from StringIO import StringIO
import re

from openn.xml.xml_whatsit import XMLWhatsit
from openn.xml.ms_item import MSItem
from openn.xml.licence import Licence
from openn.xml.resp_stmt import RespStmt
from openn.xml.related_resource import RelatedResource
from openn.xml.author import Author
from openn.xml.identifier import Identifier
from openn.openn_exception import OPennException
from openn.models import *

class OPennTEI(XMLWhatsit):
    TEI_NS            = 'http://www.tei-c.org/ns/1.0'
    fix_path_re       = re.compile('^data/')
    n_brackets_re     = re.compile('[\[\]]')
    n_open_paren_re   = re.compile('\( ')
    n_close_paren_re  = re.compile(' \)')
    n_final_comma_re  = re.compile(',\s*$')
    n_extra_spaces_re = re.compile('\s+')

    def __init__(self, xml):
        if xml is None:
            raise OPennException("XML has no content")

        if (isinstance(xml, str) or isinstance(xml, unicode)) and xml.strip() == '':
            raise OPennException("XML has no content")

        if isinstance(xml, str):
            parser = etree.XMLParser(recover=True, encoding='utf-8', remove_blank_text=True)
            self.xml = etree.fromstring(xml, parser)
        elif isinstance(xml, unicode):
            parser = etree.XMLParser(recover=True, encoding='utf-8', remove_blank_text=True)
            # self.xml = etree.parse(StringIO(xml.encode('utf-8')), parser)
            self.xml = etree.parse(StringIO(xml.encode('utf-8')), parser)
        else:
            parser = etree.XMLParser(encoding='utf-8', remove_blank_text=True)
            self.xml = etree.parse(xml, parser)
        self._namespaces = { 't': OPennTEI.TEI_NS }

    @property
    def ns(self):
        return self._namespaces

    @property
    def tei_authors(self):
        """
        If present, return the author(s) of the TEI file. This is not
        the work authors.
        """
        if not getattr(self,'_tei_authors', None):
            xpath = '//t:fileDesc/t:titleStmt/t:author'
            self._tei_authors = self._all_the_strings(xpath)
        return self._tei_authors

    @property
    def call_number(self):
        return self._get_text('//t:msIdentifier/t:idno')

    @property
    def inst_repo(self):
        a = [ self.institution, self.repository ]
        s = [ x for x in a if x ]
        return ' '.join(s).strip()

    @property
    def full_call_number(self):
        a = [ self.inst_repo, self.call_number ]
        s = [ x for x in a if x ]
        return ' '.join(s).strip()

    @property
    def formal_title(self):
        return "%s, %s" % (self.full_call_number, self.title)

    @property
    def tei_title(self):
        return self._get_text('//t:fileDesc/t:titleStmt/t:title')

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
    def collection(self):
        return self._get_text('//t:msIdentifier/t:collection')

    @property
    def country(self):
        return self._get_text('//t:msIdentifier/t:country')

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
    def date_from(self):
        return self._get_attr('//t:history/t:origin/t:origDate', 'from')

    @property
    def date_to(self):
        return self._get_attr('//t:history/t:origin/t:origDate', 'to')

    @property
    def date_when(self):
        return self._get_attr('//t:history/t:origin/t:origDate', 'when')

    @property
    def date_notAfter(self):
        return self._get_attr('//t:history/t:origin/t:origDate', 'notAfter')

    @property
    def date_notBefore(self):
        return self._get_attr('//t:history/t:origin/t:origDate', 'notBefore')

    @property
    def orig_place(self):
        return self._get_text('//t:history/t:origin/t:origPlace')

    @property
    def orig_places(self):
        return self._all_the_strings('//t:origPlace')

    @property
    def ms_items(self):
        if not getattr(self, '_ms_items', None):
            xpath = '//t:msContents/t:msItem'
            self._ms_items = [MSItem(node,self.ns) for node in self._get_nodes(xpath)]
        return self._ms_items

    @property
    def support_material(self):
        return self._get_text('//t:objectDesc/t:supportDesc/t:support/t:p')

    @property
    def related_resources(self):
        if not getattr(self, '_related_resources', None):
            xpath = '//t:notesStmt/t:note[@type="relatedResource"]'
            self._related_resources = [RelatedResource(node, self.ns) for node in self._get_nodes(xpath)]
        return self._related_resources

    @property
    def notes(self):
        if not getattr(self, '_notes', None):
            xpath = '//t:notesStmt/t:note[not(@type)]'
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
    def geosubjects(self):
        if not getattr(self, '_geosubjects', None):
            xpath = '//t:keywords[@n="subjects/geographic"]/t:term'
            self._geosubjects = self._all_the_strings(xpath)
        return self._geosubjects

    @property
    def namesubjects(self):
        if not getattr(self, '_namesubjects', None):
            xpath = '//t:keywords[@n="subjects/names"]/t:term'
            self._namesubjects = self._all_the_strings(xpath)
        return self._namesubjects

    @property
    def keywords(self):
        if not getattr(self, '_keywords', None):
            xpath = '//t:keywords[@n="keywords"]/t:term'
            self._keywords = self._all_the_strings(xpath)
        return self._keywords

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
    def funders(self):
        return self._all_the_strings('//t:titleStmt/t:funder')

    @property
    def authors(self):
        if not getattr(self, '_authors', None):
            xpath = '//t:msContents/t:msItem[1]/t:author'
            self._authors = [Author(n, self.ns) for n in self._get_nodes(xpath)]
        return self._authors

    @property
    def author_names(self):
        return [ n.name for n in self.authors ]

    @property
    def resource(self):
        return self.alt_id('resource')

    @property
    def bibid(self):
        return self.alt_id('bibid')

    def alt_id(self, id_type):
        return self._get_text('//t:msIdentifier/t:altIdentifier[@type="%s"]/t:idno' % (id_type, ))

    @property
    def related_names(self):
        if not getattr(self, '_related_names', None):
            self._related_names = [RespStmt(n,self.ns) for n in self._get_nodes('//t:msContents/t:msItem[1]/t:respStmt')]
        return self._related_names

    @property
    def alt_identifiers(self):
        nodes = self._get_nodes('//t:msIdentifier/t:altIdentifier')
        return [ Identifier(n,self.ns) for n in nodes ]

    # Foliation
    # /TEI/teiHeader/fileDesc/sourceDesc/msDesc/physDesc/objectDesc/supportDesc/foliation
    @property
    def foliation(self):
        return self._get_text('//t:supportDesc/t:foliation')

    # Layout
    # /TEI/teiHeader/fileDesc/sourceDesc/msDesc/physDesc/objectDesc/layoutDesc/layout
    @property
    def layouts(self):
        return self._all_the_strings('//t:layoutDesc/t:layout')

    # Colophon
    # /TEI/teiHeader/fileDesc/sourceDesc/msDesc/msContents/msItem/colophon
    @property
    def colophon(self):
        return self._get_text('//t:msContents/t:msItem/t:colophon')

    # Collation
    # /TEI/teiHeader/fileDesc/sourceDesc/msDesc/physDesc/objectDesc/supportDesc/collation
    @property
    def collation(self):
        return self._get_text('//t:supportDesc/t:collation/t:p')

    # Script
    # /TEI/teiHeader/fileDesc/sourceDesc/msDesc/physDesc/scriptDesc/scriptNote
    @property
    def scripts(self):
        return self._all_the_strings('//t:scriptDesc/t:scriptNote')

    @property
    def catchwords(self):
        return self._get_text('//t:collation/t:p/t:catchwords')

    # Decoration
    # /TEI/teiHeader/fileDesc/sourceDesc/msDesc/physDesc/decoDesc/decoNote
    @property
    def decoration(self):
        return self._get_text('//t:decoDesc/t:decoNote[not(@n)]')

    # Binding
    # /TEI/teiHeader/fileDesc/sourceDesc/msDesc/physDesc/bindingDesc/binding/p
    @property
    def binding(self):
        return self._get_text('//t:bindingDesc/t:binding/t:p')

    # Origin
    # /TEI/teiHeader/fileDesc/sourceDesc/msDesc/history/origin/p
    @property
    def origin(self):
        return self._get_text('//t:history/t:origin/t:p')

    # Watermarks
    # /TEI/teiHeader/fileDesc/sourceDesc/msDesc/physDesc/objectDesc/supportDesc/support/watermark
    @property
    def watermark(self):
        return self._get_text('//t:supportDesc/t:support/t:watermark')

    # Signatures
    # /TEI/teiHeader/fileDesc/sourceDesc/msDesc/physDesc/objectDesc/supportDesc/collation/p/signatures
    @property
    def signatures(self):
        return self._get_text('//t:supportDesc/t:collation/t:p/t:signatures')

    def validate(self):
        """Ensure that required attributes are present.  There are two: title
        and call_number.

        """
        errors = []

        if self.title is None or self.title.strip() == '':
            errors.append("Title (msContents/msItem/title) cannot be blank")

        if self.call_number is None or self.call_number.strip() == '':
            errors.append("Call number (msIdentifier/idno) cannot be blank")

        if len(errors) > 0:
            msg  = "TEI errors found: %s" % (', '.join(errors),)
            raise OPennException(msg)

    def fix_n(self, label):
        # normalize-space(replace(replace(replace($some-text, '[\[\]]', ''), ' \)', ')'), ',$',''))
        s = self.n_brackets_re.sub('', label)
        s = self.n_final_comma_re.sub('', s)
        s = self.n_extra_spaces_re.sub(' ', s)
        s = self.n_open_paren_re.sub('(', s)
        s = self.n_close_paren_re.sub(')', s)
        return s.strip()

    def ms_items(self, n, xml_id=None):
        if xml_id is None:
            nodes = self._get_nodes('//t:msItem[@n="%s"]' % n)
        else:
            nodes = self._get_nodes('//t:msItem/t:locus[@target="#%s"]/parent::node()' % xml_id)
        return [ MSItem(node, self.ns) for node in nodes ]

    def deco_notes(self, n, xml_id=None):
        if xml_id is None:
            nodes = [node.text for node in self._get_nodes('//t:decoNote[@n="%s"]' % n)]
        else:
            # xml.xpath('//decoNote[@n="10r"]/locus')[0].tail
            nodes = [node.tail for node in self._get_nodes('//t:decoNote/t:locus[@target="#%s"]' % xml_id)]
        # return [node.text for node in nodes ]
        return nodes

    def add_licences(self, document, license_factory):
        """
            <availability>
                <licence target="http://creativecommons.org/licenses/by/4.0/legalcode">
                    This description is ©<xsl:value-of select="year-from-date(current-date())"/>
                    University of
                    Pennsylvania Libraries. It is licensed under a Creative Commons
                    Attribution License version 4.0 (CC-BY-4.0
                    https://creativecommons.org/licenses/by/4.0/legalcode. For a
                    description of the terms of use see the Creative Commons Deed
                    https://creativecommons.org/licenses/by/4.0/. </licence>
                <licence target="http://creativecommons.org/publicdomain/mark/1.0/"> All
                    referenced images and their content are free of known copyright
                    restrictions and in the public domain. See the Creative Commons
                    Public Domain Mark page for usage details,
                    http://creativecommons.org/publicdomain/mark/1.0/. </licence>
            </availability>
        """
        xpath = '/t:TEI/t:teiHeader/t:fileDesc/t:publicationStmt/t:availability'
        for avail in self.xml.xpath(xpath, namespaces=self.ns):
            avail.getparent().remove(avail)

        availability = etree.Element("availability", nsmap=self.ns)
        lic = license_factory.license(document.image_licence)
        lic_element = etree.Element("licence", target=lic.legalcode_url(), nsmap=self.ns)
        lic_element.text = lic.format_images(**self.image_license_args(document))
        availability.append(lic_element)

        lic = license_factory.license(document.metadata_licence)
        lic_element = etree.Element("licence", target=lic.legalcode_url(), nsmap=self.ns)
        lic_element.text = lic.format_metadata(**self.metadata_license_args(document))
        availability.append(lic_element)

        pub_stmt = self.xml.xpath('/t:TEI/t:teiHeader/t:fileDesc/t:publicationStmt',
                                  namespaces=self.ns)[0]
        pub_stmt.append(availability)

    def add_funders(self, funders=[]):
        if funders is None or len(funders) == 0:
            return

        xpath = '/t:TEI/t:teiHeader/t:fileDesc/t:titleStmt'
        title_stmt = self.xml.xpath(xpath, namespaces=self.ns)[0]
        for funder in funders:
            funder_element = etree.Element('funder', nsmap=self.ns)
            funder_element.text = funder
            title_stmt.append(funder_element)

    def metadata_license_args(self, document):
        args = document.metadata_license_args()
        title = "%s %s: %s" % (self.repository, self.call_number, self.title)
        args['title'] = title

        return args

    def image_license_args(self, document):
        args = document.image_license_args()
        title = "%s, %s: %s" % (self.repository, self.call_number, self.title)
        args['title'] = title

        return args
    def add_file_list(self,document):
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
        for image in document.image_set.filter(image_type='document'):
            # n = self.fix_n(image.label)
            surface_attrs = {}
            surface_attrs['n'] = self.fix_n(image.label)
            if image.serial_number is not None:
                surface_attrs['xml:id'] = image.xml_id()
            surface_attrs['nsmap'] = self.ns
            if image.xml_id() is not None:
                surface_attrs['{http://www.w3.org/XML/1998/namespace}id'] = image.xml_id()
            # surface = etree.Element("surface", n=n, nsmap=self.ns)
            surface = etree.Element("surface", **surface_attrs)
            for deriv in image.derivative_set.all():
                deriv_type = deriv.deriv_type
                path = OPennTEI.fix_path_re.sub("", deriv.path)
                attrs = {}
                attrs['url'] = path
                attrs['width'] = "%spx" % str(deriv.width)
                attrs['height'] = "%spx" % str(deriv.height)
                graphic = etree.Element('graphic', **attrs)
                surface.append(graphic)
            facs.append(surface)
