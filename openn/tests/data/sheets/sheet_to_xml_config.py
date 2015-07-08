# -*- coding: utf-8 -*-

class SheetToXMLConfig:
    def __init__(self, sheet_attr, xml_root, *groups):
        self.sheet_attr = sheet_attr
        self.xml_root = xml_root
        self.groups = groups
