#!/usr/bin/env python

class WorkbookData:
    def __init__(self):
        self._sheet_data = {}

    def add_sheet_data(self, sheet_data):
        self._sheet_data[sheet_data.sheet_attr()] = sheet_data

    def sheet_datas(self):
        for attr in self._sheet_data:
            yield self._sheet_data[attr]

    def sheet_attrs(self):
        return [ x for x in self._sheet_data ]

    def sheet_data(self, attr):
        return self._sheet_data.get(attr, None)
