#!/usr/bin/env python

"""op-info

Print out info on object in OP database


"""
import xlrd
import sys
from optparse import OptionParser

def cmd():
    return os.path.basename(__file__)

# ------------------------------------------------------------------------------
# ACTIONS
# ------------------------------------------------------------------------------
def main(cmdline=None):
    """op-info

    """
    status = 0
    parser = make_parser()

    opts, args = parser.parse_args(cmdline)



    try:
        if len(args) != 1:
            raise Exception("Wrong number of arguments")

        path = args[0]
        book = xlrd.open_workbook(path)
        sh = book.sheet_by_index(0)
        bibid = sh.cell_value(rowx=1, colx=0)
        print int(bibid)

    except ValueError as vex:
        if bibid is None or bibid == '':
            msg = "Expected BibID cell A2 is blank in %s\n" % (path,)
            sys.stderr.write(msg)
        else:
            msg = "Unable to parse BibID is integer: %s\n" % (str(bibid,))
            sys.stderr.write(msg)

        status = 2
    except Exception as ex:
        parser.error(str(ex))
        status = 2

    return status


def make_parser():
    """ option parser"""

    usage = """%prog /path/to/MM_Metadata.xlsx

Extract the BibID from an `MM_Metadata.xlsx` file. BibID is expected
to be in cell 'A2'."""
    parser = OptionParser(usage)

    return parser

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
