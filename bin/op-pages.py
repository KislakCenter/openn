#!/usr/bin/env python

"""op-pages

Script to generate HTML files for OPenn.



"""

import glob
import os
import sys
import logging
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

def staging_dir():
    return settings.STAGING_DIR

def readme_source_path(readme):
    for tdir in settings.TEMPLATE_DIRS:
        for templ in settings.README_TEMPLATES:
            path = os.path.join(tdir, templ)
            if os.path.exists(path):
                return path

def find_readme_paths():
    paths = []
    for tdir in settings.TEMPLATE_DIRS:
        for templ in settings.README_TEMPLATES:
            path = os.path.join(tdir, templ)
            if os.path.exists(path):
                paths.append(path)

    return paths

def setup_logger():
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)-15s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    logging.getLogger().addHandler(ch)
    logging.getLogger().setLevel(logging.DEBUG)

def update_online_statuses():
    for doc in Document.objects.all():
        if doc.is_online:
            pass
        else:
            if doc.is_live():
                doc.is_online = True
                doc.save()
        logging.debug("Is document online: %s/%s? %s" % (doc.collection, doc.base_dir, str(doc.is_online)))

def browse_makeable(doc):
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

def browse_needed(doc):
    # doesn't matter if it's needed if we can't make it
    if not browse_makeable(doc):
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

def make_browse_html(docid, force=False):
    try:
        doc = Document.objects.get(pk=docid)
        make_page = browse_makeable(doc) if force else browse_needed(doc)
        outpath = os.path.join(staging_dir(), doc.browse_path)

        if make_page:
            page = Browse(doc.id, **{ 'outdir': staging_dir() })
            logging.debug("Creating page: %s" % (outpath, ))
            page.create_pages()
        else:
            logging.debug("Skipping page: %s" % (outpath, ))
    except Exception as ex:
        msg = "Error creating browse HTML for docid: '%s'; error: %s" % (str(docid), str(ex))
        raise OPennException(msg)

def toc_makeable(coll_config):
    tag = coll_config['tag']
    html_dir = os.path.join(staging_dir(), coll_config['html_dir'])
    if not os.path.exists(html_dir):
        logging.debug("No HTML dir found: %s; skipping %s" % (html_dir, tag))
        return False

    html_files = glob.glob(os.path.join(html_dir, '*.html'))
    if len(html_files) == 0:
        logging.debug("No HTML files found in %s; skipping %s" % (html_dir, tag))
        return False

    return True

def toc_needed(coll_config):
    if not toc_makeable(coll_config):
        return False

    tag = coll_config['tag']
    html_dir = os.path.join(staging_dir(), coll_config['html_dir'])
    html_files = glob.glob(os.path.join(html_dir, '*.html'))
    toc_path = os.path.join(staging_dir(), coll_config['toc_file'])
    if not os.path.exists(toc_path):
        return True

    newest_html = max([os.path.getmtime(x) for x in html_files])
    if os.path.getmtime(toc_path) > newest_html:
        logging.debug("TOC file newer than all HTML files found in %s; skipping %s" % (html_dir, tag))
        return False

    return True

def make_toc_html(coll_name, force=False):
    try:
        coll_config = settings.COLLECTIONS[coll_name]
        make_page = toc_makeable(coll_config) if force else toc_needed(coll_config)
        outpath = os.path.join(staging_dir(), coll_config['toc_file'])

        if make_page:
            toc = TableOfContents(coll_name, **{
                'template_name': 'TableOfContents.html',
                'outdir': staging_dir() })
            logging.debug("Creating TOC for collection %s: %s" % (coll_config['tag'], outpath))
            toc.create_pages()
        else:
            logging.debug("Skipping TOC for collection %s: %s" % (coll_config['tag'], outpath))
    except Exception as ex:
        msg = "Error creating TOC for: '%s'; error: %s" % (collection, str(ex))
        raise OPennException(msg)

def readme_makeable(source_path):
    return source_path and os.path.exists(source_path)

def readme_needed(source_path,outpath):
    if not readme_makeable(source_path):
        return False
    if os.path.exists(outpath):
        source_mtime = os.path.getmtime(source_path)
        out_mtime = os.path.getmtime(outpath)
        return source_mtime >= out_mtime
    else:
        return True

def make_readme_html(readme, force=False):
    try:
        source_path = readme_source_path(readme)
        outpath = os.path.join(staging_dir(), readme)

        make_page = False
        if force:
            make_page = readme_makeable(source_path)
        else:
            make_page = readme_needed(source_path, outpath)

        if make_page:
            page = Page(readme, staging_dir())
            logging.debug("Creating page: %s" % (outpath, ))
            page.create_pages()
        else:
            logging.debug("Skipping page: %s" % (outpath, ))
    except Exception as ex:
        msg = "Error creating ReadMe file: '%s'; error: %s" % (readme, str(ex))
        raise OPennException(msg)

# ------------------------------------------------------------------------------
# ACTIONS
# ------------------------------------------------------------------------------
def process_all(opts):
    browse(opts)
    toc(opts)
    readme(opts)

def browse(opts):
    # update online statuses of the Documents first
    update_online_statuses()
    docids = [doc.id for doc in Document.objects.filter(is_online = True)]
    for docid in docids:
        document(docid, opts)

def toc(opts):
    for coll in settings.COLLECTIONS:
        collection(coll, opts)

def collection(collection, opts):
    make_toc_html(collection, opts.force)

def document(docid, opts):
    make_browse_html(docid, opts.force)

def readme(opts):
    for readme in settings.README_TEMPLATES:
        readmefile(readme, opts)

def readmefile(filename,opts):
    make_readme_html(filename, opts.force)

def check_options(opts):
    # get the options
    opt_dict = vars(opts)

    # remove dry-run
    dry_run = opt_dict['dry_run']
    opt_dict['dry_run'] = False
    # remove force
    force = opt_dict['force']
    opt_dict['force'] = False

    # collect used options
    os = dict((k,opt_dict[k]) for k in opt_dict if opt_dict[k])

    if len(os) > 1:
        s = ', '.join(["%s=%s" % (k,str(v)) for k,v in os.iteritems()])
        raise OPennException("More than one option selected: %s" % (s,))

    os['dry_run'] = dry_run
    os['force'] = force

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

        if opts.browse:
            browse(opts)

        elif opts.toc:
            toc(opts)

        elif opts.readme:
            readme(opts)

        elif opts.collection:
            collection(opts)

        elif opts.document:
            document(opts.document, opts)

        elif opts.readmefile:
            readmefile(opts.readmefile, opts)

        else:
            process_all(opts)

    except OPennException as ex:
        parser.error(str(ex))
        status = 4
    except Exception as ex:
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

    parser.add_option('-b', '--browse',
                      action='store_true', dest='browse', default=False,
                      help='Process browse HTML files as needed')

    parser.add_option('-t', '--toc',
                      action='store_true', dest='toc', default=False,
                      help='Process TOC HTML files as needed')

    parser.add_option('-r', '--readme',
                      action='store_true', dest='readme', default=False,
                      help='Process ReadMe files as needed')

    parser.add_option('-m', '--readmefile', dest='readmefile', default=None,
                      help="Process ReadMe HTML for README", metavar="README")

    parser.add_option('-c', '--collection', dest='collection', default=None,
                      help="Process table of contents for COLLECTION",
                      metavar="COLLECTION")

    parser.add_option('-d', '--document', dest='document', default=None,
                      help="Process browse HTML for DOC_ID",
                      metavar="DOC_ID")


    parser.add_option('-n', '--dry-run',
                      action='store_true', dest='dry_run', default=False,
                      help='Make no changes; show what would be done [default: %default]')
    parser.add_option('-f', '--force',
                      action='store_true', dest='force', default=False,
                      help='Create all makeable files; not just those needed')

    return parser

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
