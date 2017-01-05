# -*- coding: utf-8 -*-

import os
from openn.csv.unicode_csv import UnicodeCSVWriter
import openn.openn_functions as opfunc

class OPennCSV(object):
    """docstring for OPennCSV"""
    def __init__(self, outdir, filename):
        self.outdir    = outdir
        self.filename  = filename
        self.csvfile   = None
        self.csvwriter = None
        super(OPennCSV, self).__init__()

    def outpath(self):
        return os.path.join(self.outdir, self.filename)

    def writerow(self,row):
        if self.csvwriter is None:
            self.csvwriter = UnicodeCSVWriter(self._csvfile())

        self.csvwriter.writerow(row)

    def writerows(self,rows):
        for row in rows:
            self.writerow(row)

    def close(self):
        if self.csvfile is None:
            return
        if self.csvfile.closed:
            return

        self.csvfile.close()

    def _csvfile(self):
        if self.csvfile is None:
            opfunc.ensure_dir(self.outdir)
            self.csvfile = open(self.outpath(), 'wb')

        return self.csvfile
