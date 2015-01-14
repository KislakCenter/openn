#!/usr/bin/env python

"""op-pages

Script to generate HTML files for OPenn.



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
from django.template.base import TemplateDoesNotExist

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
        logging.info("Is document online: %s/%s? %s" % (doc.collection, doc.base_dir, str(doc.is_online)))

def collection_tags():
    return [ x for x in settings.COLLECTIONS ]


def browse_makeable(doc):
    if not doc.is_online:
        logging.info("Document not online; skipping: %s/%s" % (doc.collection, doc.base_dir))
        return False

    if not (doc.tei_xml and len(doc.tei_xml) > 0):
        logging.info("Document lacks TEI; skipping: %s/%s" % (doc.collection, doc.base_dir))
        return False

    return True

def browse_needed(doc):
    # doesn't matter if it's needed if we can't make it
    if not browse_makeable(doc):
        return False
    if not doc.prepstatus.succeeded:
        logging.info("Document's last prep failed; skipping: %s/%s" % (doc.collection, doc.base_dir))
        return False

    outfile = os.path.join(staging_dir(), doc.browse_path)
    if os.path.exists(outfile):
        mtime = datetime.fromtimestamp(os.path.getmtime(outfile))
        if mtime < doc.prepstatus.started:
            return True
        else:
            logging.info("Document's HTML up-to-date; skipping: %s/%s" % (doc.collection, doc.base_dir))
            return False
    else:
        return True

def make_browse_html(docid, force=False, dry_run=False):
    try:
        doc = Document.objects.get(pk=docid)
        make_page = browse_makeable(doc) if force else browse_needed(doc)
        outpath = os.path.join(staging_dir(), doc.browse_path)

        if make_page:
            logging.info("Creating page: %s" % (outpath, ))
            if not dry_run:
                page = Browse(doc.id, **{ 'outdir': staging_dir() })
                page.create_pages()
        else:
            logging.info("Skipping page: %s" % (outpath, ))
    except Exception as ex:
        msg = "Error creating browse HTML for docid: '%s'; error: %s" % (str(docid), str(ex))
        raise OPennException(msg)

def toc_makeable(coll_config):
    tag = coll_config['tag']
    html_dir = os.path.join(staging_dir(), coll_config['html_dir'])
    if not os.path.exists(html_dir):
        logging.info("No HTML dir found: %s; skipping %s" % (html_dir, tag))
        return False

    html_files = glob.glob(os.path.join(html_dir, '*.html'))
    if len(html_files) == 0:
        logging.info("No HTML files found in %s; skipping %s" % (html_dir, tag))
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
        logging.info("TOC file newer than all HTML files found in %s; skipping %s" % (html_dir, tag))
        return False

    return True

def make_toc_html(coll_name, force=False, dry_run=False):
    try:
        coll_config = settings.COLLECTIONS[coll_name]
        make_page = toc_makeable(coll_config) if force else toc_needed(coll_config)
        outpath = os.path.join(staging_dir(), coll_config['toc_file'])

        if make_page:
            logging.info("Creating TOC for collection %s: %s" % (coll_config['tag'], outpath))
            if not dry_run:
                toc = TableOfContents(coll_name, **{
                    'template_name': 'TableOfContents.html',
                    'outdir': staging_dir() })
                toc.create_pages()
        else:
            logging.info("Skipping TOC for collection %s: %s" % (coll_config['tag'], outpath))
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

def make_readme_html(readme, force=False, dry_run=False):
    try:
        source_path = readme_source_path(readme)
        outpath = os.path.join(staging_dir(), readme)

        make_page = False
        if force:
            make_page = readme_makeable(source_path)
        else:
            make_page = readme_needed(source_path, outpath)

        if make_page:
            logging.info("Creating page: %s" % (outpath, ))
            if not dry_run:
                page = Page(readme, staging_dir())
                page.create_pages()
        else:
            logging.info("Skipping page: %s" % (outpath, ))
    except TemplateDoesNotExist as ex:
        msg = "Could not find template: %s" % (readme,)
        raise OPennException(msg)
    except Exception as ex:
        msg = "Error creating ReadMe file: '%s'; error: %s" % (readme, str(ex))
        raise OPennException(msg)

def collections_makeable(source_path):
    return source_path and os.path.exists(source_path)

def collections_needed(source_path,outpath):
    """If the collections template exits; we always say it's needed.

    Why? If implemented, the tests for creating a new collections list
    page would ask the following.  A Yes answer to any would trigger
    page generation.

    1. Is there no existing 3_Collections.html file?

    2. Is the template newer than the current 3_Collections.html file?

    3. Has the collection information in the settings file changed?

    4. Are there new TOC files for collections not listed in the
       current 3_Collections.html?

    Nos. 3 and 4 are too complicated to make it worth figuring out.

    Therefore, we always say the page is needed.

    """
    return collections_makeable(source_path)

def make_collections(opts, force=False, dry_run=False):
    try:
        source_path = readme_source_path(settings.COLLECTIONS_TEMPLATE)
        outpath = os.path.join(staging_dir(), settings.COLLECTIONS_TEMPLATE)

        make_page = False
        if force:
            make_page = collections_makeable(source_path)
        else:
            make_page = collections_needed(source_path, outpath)

        if make_page:
            logging.info("Creating list of collections: %s" % (outpath, ))
            if not dry_run:
                page = Collections(settings.COLLECTIONS_TEMPLATE, staging_dir())
                page.create_pages()
        else:
            logging.info("Skipping page: %s" % (outpath, ))
    except TemplateDoesNotExist as ex:
        msg = "Could not find template: %s" % (settings.COLLECTIONS_TEMPLATE,)
        raise OPennException(msg)
    except Exception as ex:
        msg = "Error creating ReadMe file: '%s'; error: %s" % (settings.COLLECTIONS_TEMPLATE, str(ex))
        raise OPennException(msg)

# ------------------------------------------------------------------------------
# ACTIONS
# ------------------------------------------------------------------------------
def process_all(opts):
    browse(opts)
    toc(opts)
    collections(opts)
    readme(opts)

def browse(opts):
    # update online statuses of the Documents first
    update_online_statuses()
    docids = [doc.id for doc in Document.objects.filter(is_online = True)]
    for docid in docids:
        document(docid, opts)

def toc(opts):
    for coll in settings.COLLECTIONS:
        toc_collection(coll, opts)

def toc_collection(collection_tag, opts):
    make_toc_html(collection_tag, opts.force, opts.dry_run)

def document(docid, opts):
    make_browse_html(docid, opts.force, opts.dry_run)

def readme(opts):
    for readme in settings.README_TEMPLATES:
        readme_file(readme, opts)

def readme_file(filename,opts):
    make_readme_html(filename, opts.force, opts.dry_run)

def collections(opts):
    make_collections(opts, opts.force, opts.dry_run)

def print_options(opts):
    for k in vars(opts):
        print "OPTION: %12s  %s" % (k, getattr(opts, k))


def check_options(opts):
    # get the options
    opt_dict = copy.deepcopy(vars(opts))

    # remove dry-run
    dry_run = opt_dict['dry_run']
    opt_dict['dry_run'] = False
    # remove force
    force = opt_dict['force']
    opt_dict['force'] = False
    # remove show-options
    show_options = opt_dict['show_options']
    opt_dict['show_options'] = False

    # collect used options
    os = dict((k,opt_dict[k]) for k in opt_dict if opt_dict[k])

    if len(os) > 1:
        s = ', '.join(["%s=%s" % (k,str(v)) for k,v in os.iteritems()])
        raise OPennException("More than one option selected: %s" % (s,))

    os['dry_run'] = dry_run
    os['force'] = force
    os['show_options'] = show_options

    return os

def main(cmdline=None):
    """op-pages

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

        if opts.dry_run:
            logging.warn("Performing DRY RUN")

        if opts.browse:
            browse(opts)

        elif opts.toc:
            toc(opts)

        elif opts.readme:
            readme(opts)

        elif opts.collection_tag:
            toc_collection(opts.collection_tag, opts)

        elif opts.collections:
            collections(opts)

        elif opts.document:
            document(opts.document, opts)

        elif opts.readme_file:
            readme_file(opts.readme_file, opts)

        else:
            process_all(opts)

        if opts.dry_run:
            logging.warn("DRY RUN COMPLETE; displayed actions approximate")

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

Create and stage HTML pages for OPenn.

By default all HTML page types will be generated and staged as needed in this
order:

    1. browse pages for each document on-line
    2. table of contents for each collection with documents on-line
    3. all ReadMe files

Use options for more granular behavior, to force creation of certain files, or
to do a dry run of the script.

IN MORE DETAIL
==============

If you've published a document's image files to OPenn or updated a published
document, this script will generate a browse page for it.  If a document is in
the database but its image files haven't been published to OPenn or something
went wrong with the document's preparation, then no page will be generated.  If
a document's browse page already exists and is up-to-date, then a new one won't
be regenerated.

Before browse page generation is done, %prog looks online for each
document that hasn't already been marked as being online.

A table of contents (TOC) file is generated for any collection that has
documents with published images and browse pages.  A collection's TOC file is
regenerated whenever new browse pages are added or existing ones are updated.

A ReadMe file is generated when no staged copy of the file is found or its
template is updated (thus making the staged copy out-of-date).

Note that you can force the regeneration of a file by deleting its staged copy.

The --force option will cause the system to generate any *makeable* file even if
the it doesn't "think" it needs to (on *makeable* files, see YADDA YADDA below).

THE YADDA YADDA
===============

Here's some more detailed information about how this script workds.

WHERE ARE FILES CREATED?
========================

Documents are staged according to parameters defined in `openn/settings`.  These
include the STAGING_DIR, the local directory where pages are staged for pushing
to OPenn; and collection-specific files and subdirectories as defined under
COLLECTIONS[<COLLECTION_KEY>]:

    - `toc_file`: output name of the table of contents file; e.g.,
       'TOC_LJSchoenberg_Manuscripts.html'
    - `web_dir`: output directory for browse HTML pages; e.g.,
      'Data/LJSchoenberg_Manuscripts/html'

WHEN ARE FILES CREATED?
=======================

Before creating any file the system asks the following questions and only
creates the file if the answer to both is Yes:

    - Is it *makeable*? That is, can this file be created?
    - Is a new version of this file *needed*?

Typically, a file *is needed* only if it is makeable, and (a) it hasn't already
been staged, or (b) the staged file is out-of-date.  By default %prog will
generate all *needed* files. The `--force` option will generate all *makeable*
files.

BROWSE PAGES
------------

Browse pages are *makeable* for any document:

    - whose images have been published to OPenn, and
    - whose last prep was successfully completed.

Browse pages are *needed* for a document if:

    - its HTML file hasn't yet been staged, or
    - its most recent prep is newer than the currently staged HTML file.

TABLE OF CONTENTS PAGES
-----------------------

Table of contents (TOC) files are created at the collection level.  Each TOC
file lists all published documents for a given collection.  A collection's TOC
file is *makeable" only if there is an HTML browse page for at least one of the
collection's documents.  Note that TOC generation must be run after browse page
generation to be up-to-date.  A TOC file is *needed* if it is makeable and (a) it
hasn't already been staged, or (b) if the currently staged file is older than
at least one of the staged browse HTML for the TOC file's collection.

README FILES
------------

The list of ReadMe files is taken from the application's README_TEMPLATES
setting defined in `openn/settings`.  A ReadMe file is considered *makeable* if
its source file is found in one of the application's TEMPLATE_DIRS as defined in
`openn/settings.py`.  A ReadMe file is *needed* when its source file is newer
than the currently staged HTML file.

OPTIONS
=======

Except for --dry-run and --force, options may not be combined.

Note that --dry-run may show inaccurate information for TOC files.  An actual
run may create new browse files that would trigger TOC generation.  Dry runs
don't create new or update browse files, so the TOC steps will likely report
skipped TOC creation for files that would be generated for an actual run.

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

    parser.add_option('-m', '--readme-file', dest='readme_file', default=None,
                      help=("Process ReadMe HTML for README; one of:\n  %s" % (
                          ', '.join(settings.README_TEMPLATES), )),
                      metavar="README")

    parser.add_option('-i', '--toc-collection', dest='collection_tag', default=None,
                      help=("Process table of contents for COLLECTION_TAG; one of: %s" % (
                          ', '.join(collection_tags()))),
                      metavar="COLLECTION_TAG")

    parser.add_option('-d', '--document', dest='document', default=None,
                      help="Process browse HTML for DOC_ID",
                      metavar="DOC_ID")

    parser.add_option('-c', '--collections',
                      action='store_true', dest='collections', default=False,
                      help='Process Collections list HTML as needed')


    parser.add_option('-n', '--dry-run',
                      action='store_true', dest='dry_run', default=False,
                      help='Make no changes; show what would be done')
    parser.add_option('-f', '--force',
                      action='store_true', dest='force', default=False,
                      help='Create all makeable files; not just as needed')
    parser.add_option('-o', '--show-options',
                      action='store_true', dest='show_options', default=False,
                      help='Print out the options at runtime')

    return parser

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
