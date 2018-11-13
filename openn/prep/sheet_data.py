#!/usr/bin/env python

import re

from copy import deepcopy

class SheetData:

    def __init__(self, name, data_dict):
        self._sheet_name = name
        self._sheet_attr = re.sub(r'\W+', '', str(name)).lower()
        self._sheet_data = deepcopy(data_dict)

    def sheet_name(self):
        return self._sheet_name

    def sheet_attr(self):
        return self._sheet_attr

    def values(self, attr):
        return self._sheet_data.get(attr, [])

    def is_empty(self, attr):
        return len(self.values(attr)) == 0

    def is_present(self, attr):
        return not self.is_empty()

    def paired_values(self, attr, other_attr):
        return self.value_matrix(attr, other_attr)

    def values_dict(self, *attrs):
        matrix = self.value_matrix(*attrs)
        vdict = {}
        for i in xrange(len(attrs)):
            vdict[attrs[i]] = matrix[i]

        return vdict

    def value_matrix(self, *attrs):
        matrix = [ deepcopy(self.values(x)) for x in attrs ]
        # Find each None item in the list; replace with []
        for i in xrange(len(matrix)):
            if matrix[i] is None:
                matrix[i] = []
        max_len = len(max(matrix, key=lambda x: len(x)))
        for values in matrix:
            if len(values) < max_len:
                values.extend([ None ] * (max_len - len(values)))
        return matrix

    def composite_values(self, *attrs):
        values = []
        mtx = self.value_matrix(*attrs)
        for row in zip(*mtx):
            v = [ unicode(x) for x in row if x ]
            values.append(' '.join(v))

        return values
