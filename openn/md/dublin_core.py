# -*- coding: utf-8 -*-
class DublinCore(object):

    def to_dict(self):
        dc                   = {}
        dc['dc:contributor'] = self.dc_contributor()
        dc['dc:coverage']    = self.dc_coverage()
        dc['dc:creator']     = self.dc_creator()
        dc['dc:date']        = self.dc_date()
        dc['dc:description'] = self.dc_description()
        dc['dc:format']      = self.dc_format()
        dc['dc:identifier']  = self.dc_identifier()
        dc['dc:language']    = self.dc_language()
        dc['dc:publisher']   = self.dc_publisher()
        dc['dc:relation']    = self.dc_relation()
        dc['dc:rights']      = self.dc_rights()
        dc['dc:source']      = self.dc_source()
        dc['dc:subject']     = self.dc_subject()
        dc['dc:title']       = self.dc_title()
        dc['dc:type']        = self.dc_type()
        dc['dc:contributor'] = self.dc_contributor()
        dc['dc:coverage']    = self.dc_coverage()
        dc['dc:creator']     = self.dc_creator()
        dc['dc:date']        = self.dc_date()
        dc['dc:description'] = self.dc_description()
        dc['dc:format']      = self.dc_format()
        dc['dc:identifier']  = self.dc_identifier()
        dc['dc:language']    = self.dc_language()
        dc['dc:publisher']   = self.dc_publisher()
        dc['dc:relation']    = self.dc_relation()
        dc['dc:rights']      = self.dc_rights()
        dc['dc:source']      = self.dc_source()
        dc['dc:subject']     = self.dc_subject()
        dc['dc:title']       = self.dc_title()
        dc['dc:type']        = self.dc_type()

        return dict((k,v) for k,v in dc.items() if v and len(v) > 0)

    def dc_contributor(self):
        return None

    def dc_coverage(self):
        return None

    def dc_creator(self):
        return None

    def dc_date(self):
        return None

    def dc_description(self):
        return None

    def dc_format(self):
        return None

    def dc_identifier(self):
        return None

    def dc_language(self):
        return None

    def dc_publisher(self):
        return None

    def dc_relation(self):
        return None

    def dc_rights(self):
        return None

    def dc_source(self):
        return None

    def dc_subject(self):
        return None

    def dc_title(self):
        return None

    def dc_type(self):
        return None
