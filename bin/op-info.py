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

def update_online_statuses():
    for doc in Document.objects.all():
        if doc.is_online:
            pass
        else:
            if doc.is_live():
                doc.is_online = True
                doc.save()
        logging.info("Is document online: %s/%s? %s" % (doc.collection, doc.base_dir, str(doc.is_online)))

def setup_logger():
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)-15s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    logging.getLogger().addHandler(ch)
    logging.getLogger().setLevel(logging.DEBUG)


def print_options(opts):
    for k in vars(opts):
        print "OPTION: %12s  %s" % (k, getattr(opts, k))

def update_online_statuses():
    for doc in Document.objects.all():
        if doc.is_online:
            pass
        else:
            if doc.is_live():
                doc.is_online = True
                doc.save()
        logging.info("Is document online: %s/%s? %s" % (doc.collection, doc.base_dir, str(doc.is_online)))

def check_options(opts):
    pass

# ------------------------------------------------------------------------------
# ACTIONS
# ------------------------------------------------------------------------------
def show_all(opts):
    pass

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

    try:
        check_options(opts)

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

    parser.add_option('-o', '--show-options',
                      action='store_true', dest='show_options', default=False,
                      help='Print out the options at runtime')
    return parser

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
