#!/usr/bin/env python

"""op-pages

Script to generate HTML files for OPenn.



"""


from optparse import OptionParser
import os
from distutils.dir_util import copy_tree
import sys
import logging
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

def staging_dir():
    return settings.STAGING_DIR

def setup_logger():
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)-15s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    logging.getLogger().addHandler(ch)
    logging.getLogger().setLevel(logging.DEBUG)

def do_online_prep():
    for doc in Document.objects.all():
        if doc.is_online:
            pass
        else:
            if doc.is_live():
                doc.is_online = True
                doc.save()
        logging.debug("Is document online: %s/%s? %s" % (doc.collection, doc.base_dir, str(doc.is_online)))

def html_makeable(doc):
    if doc.is_online:
        pass
    else:
        logging.debug("Document not online; skipping: %s/%s" % (doc.collection, doc.base_dir))
        return False

    if doc.tei_xml and len(doc.tei_xml) > 0:
        pass
    else:
        logging.debug("Document lacks TEI; skipping: %s/%s" % (doc.collection, doc.base_dir))
        return False

    return True

def html_needed(doc):
    # doesn't matter if it's needed if we can't make it
    if not html_makeable(doc):
        return False
    if not doc.prepstatus.succeeded:
        logging.debug("Document's last prep failed; skipping: %s/%s" % (doc.collection, doc.base_dir))
        return False

    outfile = os.path.join(staging_dir(), doc.browse_path)
    if os.path.exists(outfile):
        mtime = datetime.fromtimestamp(os.path.getmtime(outfile))
        if mtime < doc.prepstatus.started:
            return True
        else:
            logging.debug("Document's HTML up-to-date; skipping: %s/%s" % (doc.collection, doc.base_dir))
            return False
    else:
        return True

def make_browse_html(doc, force=False):
    make_page = html_makeable(doc) if force else html_needed(doc)
    logpath = os.path.join(staging_dir(), doc.browse_path)

    if make_page:
        page = Browse(doc.id, **{ 'outdir': staging_dir() })
        logging.debug("Creating page: %s" % (logpath, ))
        page.create_pages()
    else:
        logging.debug("Skipping page: %s" % (logpath, ))

# ------------------------------------------------------------------------------
# ACTIONS
# ------------------------------------------------------------------------------
def process_all(opts):
    browse(opts)

def force_all(opts):
    print "Option --all-force selected"

def browse(opts):
    pages = []
    do_online_prep()
    for doc in Document.objects.filter(is_online = True):
        make_browse_html(doc)

def force_browse(opts):
    print "Option --browse-force selected"

def toc(opts):
    print "Option --toc selected"

def force_toc(opts):
    print "Option --toc-force selected"

def collection(opts):
    print "Option --collection=%s selected" % (opts.collection, )

def force_collection(opts):
    print "Option --collection-force=%s selected" % (opts.force_collection, )

def force_document(opts):
    print "Option --document-force=%s selected" % (opts.force_document, )

def document(opts):
    print "Option --document=%s selected" % (opts.document, )

def readme(opts):
    print "Option --readme selected"

def force_readme(opts):
    print "Option --readme-force selected"

def check_options(opts):
    # get the options
    opt_dict = vars(opts)

    # remove dry-run
    dry_run = opt_dict['dry_run']
    del opt_dict['dry_run']

    # collect used options
    os = dict((k,opt_dict[k]) for k in opt_dict if opt_dict[k])

    if len(os) > 1:
        s = ', '.join(["%s=%s" % (k,str(v)) for k,v in os.iteritems()])
        raise OPennException("More than one option selected: %s" % (s,))

    if dry_run:
        os['dry_run'] = dry_run

    return os

def main(cmdline=None):
    """op-pages

    """
    status = 0
    parser = make_parser()

    opts, args = parser.parse_args(cmdline)

    setup_logger()
    logger = logging.getLogger(__name__)

    try:
        check_options(opts)

        if opts.force_all:
            force_all(opts)

        elif opts.browse:
            browse(opts)
        elif opts.force_browse:
            force_browse(opts)

        elif opts.toc:
            toc(opts)
        elif opts.force_toc:
            force_toc(opts)

        elif opts.readme:
            readme(opts)
        elif opts.force_readme:
            force_readme(opts)

        elif opts.collection:
            collection(opts)
        elif opts.force_collection:
            force_collection(opts)

        elif opts.document:
            document(opts)
        elif opts.force_document:
            force_document(opts)

        else:
            process_all(opts)

    except OPennException as ex:
        parser.error(str(ex))
        status = 4

    return status
    # try:
    #     pages = []
    #     outdir = settings.STAGING_DIR
    #     html_dir = os.path.join(settings.STAGING_DIR, 'html')
    #     if not os.path.exists(html_dir):
    #         os.makedirs(html_dir)
    #     this_dir = os.path.dirname(__file__)
    #     copy_tree(os.path.join(this_dir, '..', 'openn/templates/html'), html_dir)
    #     pages.append(Page('0_ReadMe.html', outdir))
    #     pages.append(Page('1_TechnicalReadMe.html', outdir))
    #     pages.append(Collections('3_Collections.html', outdir))
    #     for collection in settings.COLLECTIONS:
    #         toc = TableOfContents(collection, **{
    #             'template_name': 'TableOfContents.html',
    #             'outdir': outdir
    #         })
    #         pages.append(toc)
    #     for doc in Document.objects.all():
    #         pages.append(Browse(doc.id, **{ 'outdir': outdir }))
    #     for page in pages:
    #         page.create_pages()
    # except OPennException as ex:
    #     # error_no_exit(cmd(), str(ex))
    #     status = 4
    #     parser.error(str(ex))


def make_parser():
    """ option parser"""

    usage = """%prog [OPTIONS]

Update HTML pages for OPenn.

By default page types (browse, TOC, ReadMe) will be generated as
needed. Use options to change behavior.

Except for --dry-run, options may not be combined.
"""

    parser = OptionParser(usage)

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

    parser.add_option('-r', '--readme',
                      action='store_true', dest='readme', default=False,
                      help='Process ReadMe files as needed [default: %default]')
    parser.add_option('-R', '--readme-force',
                      action='store_true', dest='force_readme', default=False,
                      help='Force process all ReadMe files [default: %default]')

    parser.add_option('-c', '--collection', dest='collection', default=None,
                      help="Process table of contents for COLLECTION [default=%default]",
                      metavar="COLLECTION")
    parser.add_option('-C', '--collection-force', dest='force_collection', default=None,
                      help="Force process table of contents for COLLECTION [default=%default]",
                      metavar="COLLECTION")

    parser.add_option('-d', '--document', dest='document', default=None,
                      help="Process browse HTML for DOC_ID [default=%default]",
                      metavar="DOC_ID")
    parser.add_option('-D', '--document-force', dest='force_document', default=None,
                      help="Force process browse HTML for DOC_ID [default=%default]",
                      metavar="DOC_ID")

    parser.add_option('-n', '--dry-run',
                      action='store_true', dest='dry_run', default=False,
                      help='Make no changes; show what would be done [default: %default]')

    return parser

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
