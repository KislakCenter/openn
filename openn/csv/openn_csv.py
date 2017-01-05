# -*- coding: utf-8 -*-

import os
from openn.csv.unicode_csv import UnicodeCSVWriter
import openn.openn_functions as opfunc

class OPennCSV(object):
    """

    Base class for generating CSV a file. Child classes should override the
    methods write_file(),  is_makeable(), and is_needed(), as appropropiate.

    Typical usage:

        csv = OPennCSV('path/to/dir', 'file.csv')
        csv.writerow(['a', 'b', 'c'])
        csv.writerow([1, 2, 3])
        csv.close() # important; close the output file object

    """
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
    """
    If output file object exists and is not closed, close it; otherwise,
    do nothing.
    """

        if self.csvfile is None:
            return
        if self.csvfile.closed:
            return

        self.csvfile.close()

    def is_makeable(self):
        """Always return True. Method should be overridden by
            implementing class."""

        return True

    def write_file(self):
        """ Implementing classes should override this method.
        """
        pass

    def is_needed(self):
        """ Return False if is_makeable() returns false. Otherwise, return
        True. Implmenting classes should override. """
        if not self.is_makeable():
            return False

        return True

    def _csvfile(self):
        if self.csvfile is None:
            opfunc.ensure_dir(self.outdir)
            self.csvfile = open(self.outpath(), 'wb')

        return self.csvfile
