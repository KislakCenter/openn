#!/usr/bin/env python

"""op-pages

Script to generate HTML files for OPenn.



"""


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
    """op-pages



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

Update HTML pages OPenn.  """

    parser = OptionParser(usage)

    parser.add_option('-a', '--all',
                      action='store_true', dest='all_as_needed', default=True,
                      help='Process all HTML files (browse, TOC, ReadMe) as needed [default: %default]')

    parser.add_option('-A', '--all-force',
                      action='store_true', dest='force_all', default=False,
                      help='Force process all HTML files (browse, TOC, ReadMe) [default: %default]')

    parser.add_option('-b', '--browse',
                      action='store_true', dest='browse', default=False,
                      help='Process browse HTML files as needed [default: %default]')

    parser.add_option('-B', '--browse-force',
                      action='store_true', dest='force_browse', default=False,
                      help='Force process all browse HTML files [default: %default]')

    parser.add_option('-t', '--toc',
                      action='store_true', dest='toc', default=False,
                      help='Process TOC HTML files as needed [default: %default]')

    parser.add_option('-T', '--toc-force',
                      action='store_true', dest='force_toc', default=False,
                      help='Force process all TOC HTML files [default: %default]')

    parser.add_option('-n', '--dry-run',
                      action='store_true', dest='dry_run', default=False,
                      help='Make no changes; show what would be done [default: %default]')

    parser.add_option('-c', '--collection', dest='collection', default=None,
                      help="Force process table of contents for CONTENTS [default=%default]",
                      metavar="COLLECTION")


    parser.add_option('-d', '--document-id', dest='doc_id', default=None,
                      help="Force process browse HTML for DOC_ID [default=%default]",
                      metavar="DOC_ID")

    return parser

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
