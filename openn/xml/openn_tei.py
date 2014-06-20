from lxml import etree

class OPennTEI:
    TEI_NS = 'http://www.tei-c.org/ns/1.0'
    
    def __init__(self, tei_path, mode='r'):
        self.tei = etree.parse(open(tei_path, mode))
        self._namespaces = { 't': OPennTEI.TEI_NS }

    @property
    def ns(self):
        return self._namespaces

    @property
    def call_number(self):
        xpath = '//t:msIdentifier/t:idno'
        return self.tei.xpath(xpath, namespaces=self.ns)[0].text
