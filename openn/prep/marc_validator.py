# -*- coding: utf-8 -*-
from lxml import etree

class MarcValidator(object):
    """For the provided set of requirements validate a give MARC 21 XML file."""
    def __init__(self, xml_io, required_xpaths = None, holdings_id = None):
        super(MarcValidator, self).__init__()
        self.tree = etree.parse(xml_io)
        self.required_xpaths = required_xpaths
        self.holdings_id = holdings_id
        self.namespaces = { 'marc': 'http://www.loc.gov/MARC21/slim' }
        self.errors = []

    def validate(self):
        del self.errors[:] # clear the errors array

        self.validate_shelfmark()
        self.validate_required_xpaths()
        return len(self.errors) == 0

    def validate_required_xpaths(self):
        if self.required_xpaths is None:
            return

        for xpath in self.required_xpaths:
            if len(self.tree.xpath(xpath, namespaces=self.namespaces)) < 1:
                self.errors.append("Required XML not found: '%s'" % (xpath,))

        self.validate_shelfmark()

    def validate_shelfmark(self):
        if self.holdings_id  is None:
            xpath = "//marc:holding/marc:call_number/text()"
            call_numbers = self.tree.xpath(xpath, namespaces=self.namespaces)
            if len(call_numbers) < 1:
                # no holdings; assume this is not Penn MARC
                xpath = "//marc:record/marc:datafield[@tag='500']/marc:subfield[@code='a' and starts-with(text(), 'Shelfmark:')]"
                call_numbers = self.tree.xpath(xpath, namespaces=self.namespaces)
                if len(call_numbers) < 1:
                    xpath = "//marc:record/marc:datafield[@tag='099']/marc:subfield[@code='a']"
                    call_numbers = self.tree.xpath(xpath, namespaces=self.namespaces)
                    if len(call_numbers) < 1:
                        self.errors.append('No call number found in in MARC XML')
            elif len(call_numbers) > 1:
                self.errors.append('Please provide holding ID; more than one call number found in MARC XML')
        else:
            xpath = "//marc:holding_id[text() = '%s']/parent::marc:holding/marc:call_number/text()" % self.holdings_id
            call_numbers = self.tree.xpath(xpath, namespaces=self.namespaces)
            if len(call_numbers) != 1:
                self.errors.append('Expected 1 call number for holding ID %s; found %d in Penn MARC XML' % (self.holdings_id, len(call_numbers)))
