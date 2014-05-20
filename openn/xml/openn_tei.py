from lxml import etree

class OPennTei():
    def __init__(self, tei_path, mode='r'):
        self.tei = etree.parse(open(tei_path, mode))

    def shelf_mark(self):
        return self.tei.xpath('//t:msIdentifier/t:idno', 
                namespaces={ 't': 'http://www.tei-c.org/ns/1.0' })[0].text


