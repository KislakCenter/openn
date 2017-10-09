# -*- coding: utf-8 -*-
from lxml import etree
from StringIO import StringIO
import re

from openn.xml.xml_whatsit import XMLWhatsit

class OPennXML(XMLWhatsit):
    def __init__(self, xml):
        if isinstance(xml, str):
            parser = etree.XMLParser(recover=True, encoding='utf-8', remove_blank_text=True)
            self.xml = etree.fromstring(xml, parser)
        elif isinstance(xml, unicode):
            parser = etree.XMLParser(recover=True, encoding='utf-8', remove_blank_text=True)
            self.xml = etree.parse(StringIO(xml.encode('utf-8')), parser)
        else:
            parser = etree.XMLParser(encoding='utf-8', remove_blank_text=True)
            self.xml = etree.parse(xml, parser)

    def image_licence(self):
        return self._get_text('//image_rights/image_rights')

    def image_copyright_holder(self):
        return self._get_text('//image_rights/image_copyright_holder')

    def image_copyright_year(self):
        return self._get_text('//image_rights/image_copyright_year')

    def image_rights_more_info(self):
        return self._get_text('//image_rights/image_rights_more_info')

    def metadata_licence(self):
        return self._get_text('//metadata_rights/metadata_rights')

    def metadata_copyright_holder(self):
        return self._get_text('//metadata_rights/metadata_copyright_holder')

    def metadata_copyright_year(self):
        return self._get_text('//metadata_rights/metadata_copyright_year')

    def metadata_rights_more_info(self):
        return self._get_text('//metadata_rights/metadata_rights_more_info')

    def page_count(self):
        return len(self._get_nodes('//pages/page'))

    def has_serial_numbers(self):
        return len(self._get_nodes('//pages/page/serial_number')) > 0

    def page_dict(self):
        return self._get_dict('//pages')

    def page_objects(self):
        return self._get_objects('//pages/page')
