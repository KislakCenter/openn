#!/usr/bin/env python

class WorkbookData:
    def __init__(self):
        self._sheet_data = []

    def add_sheet_data(self, sheet_data):
        self._sheet_data.append(sheet_data)
        # self._sheet_data[sheet_data.sheet_attr()] = sheet_data

    def sheet_datas(self):
        return list(self._sheet_data)