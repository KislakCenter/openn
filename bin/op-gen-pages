#!/usr/bin/env python

from optparse import OptionParser
import os
from distutils.dir_util import copy_tree
import sys

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

def main(cmdline=None):
    """op-prep main
    """
    status = 0
    parser = make_parser()

    opts, args = parser.parse_args(cmdline)

    try:
        pages = []
        outdir = settings.STAGING_DIR
        html_dir = os.path.join(settings.STAGING_DIR, 'html')
        if not os.path.exists(html_dir):
            os.makedirs(html_dir)
        this_dir = os.path.dirname(__file__)
        copy_tree(os.path.join(this_dir, '..', 'openn/templates/html'), html_dir)
        pages.append(Page('0_ReadMe.html', outdir))
        pages.append(Page('1_TechnicalReadMe.html', outdir))
        pages.append(Collections('3_Collections.html', outdir))
        for collection in settings.COLLECTIONS:
            toc = TableOfContents(collection, **{
                'template_name': 'TableOfContents.html',
                'outdir': outdir
            })
            pages.append(toc)
        for doc in Document.objects.all():
            pages.append(Browse(doc.id, **{ 'outdir': outdir }))
        for page in pages:
            page.create_pages()
    except OPennException as ex:
        # error_no_exit(cmd(), str(ex))
        status = 4
        parser.error(str(ex))

    return status


def make_parser():
    """get_xml option parser"""

    usage = """%prog

Update all the pages for objects in OPenn

"""

    parser = OptionParser(usage)

    return parser

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
