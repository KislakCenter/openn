#!/usr/bin/env python

"""op-info

Print out info on object in OP database


"""

import glob
import os
import sys
import logging
import copy
from distutils.dir_util import copy_tree
from optparse import OptionParser
from datetime import datetime

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "openn.settings")
from openn.models import *
from django.core import serializers
from django.conf import settings

from openn.openn_exception import OPennException
from openn.openn_functions import *
from openn.pages.page import Page
from openn.pages.collections import Collections
from openn.pages.table_of_contents import TableOfContents
from openn.pages.browse import Browse


def cmd():
    return os.path.basename(__file__)

def setup_logger():
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)-15s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    logging.getLogger().addHandler(ch)
    logging.getLogger().setLevel(logging.DEBUG)

def add_prep(doc):
    prepstatus = PrepStatus(document=doc)
    if doc.is_online:
        prepstatus.succeeded = True
    else:
        prepstatus.succeeded = False
        prepstatus.error = 'Unknown; bulkset by %s' % (cmd(), )

    prepstatus.finished = datetime.now()
    prepstatus.save()

def add_missing_preps():
    for doc in Document.objects.all():
        if hasattr(doc, 'prepstatus'):
            logging.info("Doc already has prep: %d: %s/%s" % (doc.id, doc.collection, doc.base_dir))
        else:
            add_prep(doc)

def update_online_statuses():
    for doc in Document.objects.filter(is_online=False):
        if doc.is_live():
            doc.is_online = True
            doc.save()
        logging.info("Is document online: %s/%s? %s" % (doc.collection, doc.base_dir, str(doc.is_online)))

def print_options(opts):
    for k in vars(opts):
        print "OPTION: %12s  %s" % (k, getattr(opts, k))

def check_options(opts):
    pass


class ReportSegment:
    def __init__(self, attr=None, fmt='s', width=10, head=None):
        "docstring"
        self._attr = attr
        self._fmt = fmt
        self._width = width
        self._head = head

    def heading(self):
        return self._head or self._attr

    def header_fmt(self):
        return '%-{0}s'.format(self._width)

    def line_fmt(self):
        return '%-{0}{1}'.format(self._width,self._fmt)

    def fix_value(self, val):
        if self._fmt == 's' and val and len(str(val)) > self._width:
            return '%s...' % (val[:-3], )
        else:
            return val

    def get_val(self, obj, attr):
        item = obj
        for a in attr.split('.'):
            try:
                item = getattr(item, a)
            except AttributeError:
                item = None

        return item

    def line_val(self, obj):
        s = None

        if isinstance(obj, dict) and self._attr in obj:
            s = obj[self._attr]
        elif hasattr(obj, self._attr):
            s = getattr(obj, self._attr)

        if s:
            return self.fix_value(s)
        else:
            return ''

    def divider(self, char='-'):
        return ''.join([char for i in xrange(self._width)])

class Report:
    def __init__(self, colsep=' '):
        self._colsep = colsep
        self._segments = []

    def headings(self):
        return [x.heading() for x in self._segments]

    def header_fmt(self):
        return self._colsep.join([x.header_fmt() for x in self._segments])

    def line_fmt(self):
        return self._colsep.join([x.line_fmt() for x in self._segments])

    def divider(self, char='-'):
        return self._colsep.join([x.divider() for x in self._segments])

    def header(self):
        return self.header_fmt() % tuple(self.headings())

    def add(self, report_segment):
        self._segments.append(report_segment)

    def line_vals(self, obj):
        return [x.line_val(obj) for x in self._segments]

    def row(self,obj):
        return self.line_fmt() % tuple(self.line_vals(obj))

# ------------------------------------------------------------------------------
# ACTIONS
# ------------------------------------------------------------------------------
def show_all(opts):
    report = Report(colsep=' | ')
    report.add(ReportSegment(attr='id', fmt='d', width=4, head='ID'))
    report.add(ReportSegment(attr='collection', fmt='s', width=20, head='Coll'))
    report.add(ReportSegment(attr='base_dir', fmt='s', width=20, head='Directory'))
    report.add(ReportSegment(attr='is_online', fmt='s', width=7, head='Online?'))
    report.add(ReportSegment(attr='is_prepped', fmt='s', width=8, head='Prepped?'))
    report.add(ReportSegment(attr='created', fmt='s', width=19, head='Created'))
    report.add(ReportSegment(attr='updated', fmt='s', width=19, head='Updated'))

    print report.header()
    print report.divider()
    for doc in Document.objects.all():
        print report.row(doc)

def collections(opts):
    report = Report(colsep=' | ')
    report.add(ReportSegment(attr='tag', fmt='s', width=20))
    report.add(ReportSegment(attr='name', fmt='s', width=50))

    print report.header()
    print report.divider()
    for coll in settings.COLLECTIONS:
        h = settings.COLLECTIONS[coll]
        # print h
        print report.row(h)

def check_online(opts):
    update_online_statuses()

def set_preps(opts):
    check_online(opts)
    add_missing_preps()

def main(cmdline=None):
    """op-info

    """
    status = 0
    parser = make_parser()

    opts, args = parser.parse_args(cmdline)
    if opts.show_options:
        print_options(opts)

    setup_logger()
    logger = logging.getLogger(__name__)

    # check_options(opts)
    # show_all(opts)
    try:
        check_options(opts)

        if opts.check_online:
            check_online(opts)
            show_all(opts)
        elif opts.set_preps:
            logging.info('Runing --set-preps')
            logging.info('Pre check status')
            show_all(opts)
            print ''
            set_preps(opts)
            print ''
            show_all(opts)
        elif opts.collections:
            collections(opts)
        else:
            show_all(opts)

    except OPennException as ex:
        parser.error(str(ex))
        status = 4
    except Exception as ex:
        parser.error(str(ex))
        status = 4

    return status


def make_parser():
    """ option parser"""

    usage = """%prog [OPTIONS]

Print or update statistics about OPenn documents.

By default prints summary information about each document.
"""
    parser = OptionParser(usage)

    parser.add_option('-s', '--show-options',
                      action='store_true', dest='show_options', default=False,
                      help='Print out the options at runtime')

    parser.add_option('-o', '--check-online',
                      action='store_true', dest='check_online', default=False,
                      help='Before running update the online status of docments')

    parser.add_option('-p', '--set-preps',
                      action='store_true', dest='set_preps', default=False,
                      help='Fill in any missing prep objects based on online status')

    parser.add_option('-c', '--collections',
                      action='store_true', dest='collections', default=False,
                      help='List known collections')

    return parser

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
