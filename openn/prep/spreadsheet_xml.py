# -*- coding: utf-8 -*-

from xml.dom.minidom import parseString
from dict2xml import dict2xml

class SpreadsheetXML:

    def build_xml(self, op_workbook, xml_config):
        structure = self.build_dict(op_workbook, xml_config)
        xml       = dict2xml(structure, wrap='doc')
        return xml
        # return structure

    def build_dict(self,op_workbook,xml_config):
        structure = {}
        for sheet_config in xml_config:
            data = self.build_sheet_dict(op_workbook, sheet_config)
            structure[sheet_config['sheet_root']] = data
        return structure

    def build_sheet_dict(self, op_workbook, sheet_config):
        sheet_attr = sheet_config['sheet_attr']
        sheet_dict = {}
        for group_config in sheet_config['field_groups']:
            group_dict = self.build_group_dict(op_workbook, sheet_attr, group_config)
            group_attr = group_config['xml_attr']
            if group_dict is not None and len(group_dict) > 0:
                sheet_dict[group_attr] = group_dict
        return sheet_dict

    def build_group_dict(self, op_workbook, sheet_attr, group_config):
        spreadsheet = op_workbook.get_sheet(sheet_attr)
        columns     = group_config['columns']
        values_dict = spreadsheet.values_dict(*columns)
        group_list  = []
        for i in xrange(len(values_dict[columns[0]])):
            ele = {}
            for col in columns:
                value = values_dict[col][i]
                if value is not None: ele[col] = value
            if ele is not None and len(ele) > 0:
                group_list.append(ele)
        return group_list
