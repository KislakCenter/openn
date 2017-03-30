# -*- coding: utf-8 -*-
import re
from copy import deepcopy

from xml.dom.minidom import parseString
from dict2xml import dict2xml

class SpreadsheetXML(object):
    RIGHTS_RE          = re.compile(r'^(image|metadata)_rights$', re.IGNORECASE)

    def __init__(self, licence_config):
        self._licences = deepcopy(licence_config)

    def build_xml(self, workbook_data, xml_config):
        structure = self.build_dict(workbook_data, xml_config)
        xml       = dict2xml(structure, wrap='doc')
        return xml

    def build_dict(self,workbook_data,xml_config):
        structure = {}
        for sheet_config in xml_config:
            attr = sheet_config['sheet_attr']
            sheet_data = workbook_data.sheet_data(attr)
            data = self.build_sheet_dict(sheet_data, sheet_config)
            structure[sheet_config['sheet_root']] = data
        return structure

    def build_sheet_dict(self, sheet_data, sheet_config):
        sheet_dict = {}
        for group_config in sheet_config['field_groups']:
            group_dict = self.build_group_dict(sheet_data, sheet_config, group_config)
            group_attr = group_config['xml_attr']
            if group_dict is not None and len(group_dict) > 0:
                sheet_dict[group_attr] = group_dict

        return sheet_dict

    def build_group_dict(self, sheet_data, sheet_config, group_config):
        sheet_attr  = sheet_config['sheet_attr']

        composites  = self.composite_fields(sheet_config, sheet_data)
        columns     = group_config['columns']
        values_dict = sheet_data.values_dict(*columns)
        group_list  = []
        for i in xrange(len(values_dict[columns[0]])):
            ele = {}
            for col in columns:
                value = values_dict[col][i]
                if value is not None: ele[col] = value
            if ele is not None and len(ele) > 0:
                group_list.append(ele)
        group_attr  = group_config['xml_attr']
        if group_attr == 'page':
            self.rewrite_tags(group_list)

        return group_list

    def composite_fields(self, sheet_config, sheet_data):
        if not sheet_config.get('composite_fields', False): return {}
        field_values = {}
        comp_fields = sheet_config['composite_fields']

        for field in comp_fields:
            field_values[field] = sheet_data.composite_values(*comp_fields[field])

        return field_values

    def rewrite_tags(self, page_list):
        if page_list is None or len(page_list) == 0: return

        for page in page_list:
            tags = []
            for i in xrange(1,5):
                t = "tag" + str(i)
                v = "value" + str(i)
                if page.get(t, None) is not None:
                    tags.append({ 'name': page[t], 'value': page.get(v, None) })
                    del page[t]
                    if v in page: del page[v]
            if len(tags) > 0:
                page['tags'] = { 'tag': tags }

    def merge_dicts(self, list_of_dicts):
        if list_of_dicts is None: return {}

        merged = {}
        for d in list_of_dicts: merged.update(d)

        return merged
