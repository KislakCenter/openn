#!/usr/bin/env python

"""op-pages

Script to generate HTML files for OPenn.

"""
import glob
import os
import sys
import logging
import copy
import traceback
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
import openn.openn_functions as opfunc
from openn.pages.page import Page
from openn.repository.configs import Configs
from openn.pages.repositories import Repositories
from openn.pages.table_of_contents import TableOfContents
from openn.pages.curated_collection_toc import CuratedCollectionTOC
from openn.pages.curated_collections import CuratedCollections
from openn.pages.browse import Browse
from openn.csv.collections_csv import CollectionsCSV
from openn.csv.table_of_contents_csv import TableOfContentsCSV
from openn.csv.curated_collection_contents_csv import CuratedCollectionContentsCSV

logger = logging.getLogger(__name__)

def cmd():
    return os.path.basename(__file__)

def repository_configs():
    return Configs(settings.REPOSITORIES)

def get_repo_wrapper(tag):
    return repository_configs().get_repository(tag)

def curated_tags():
    return [x.tag for x in  CuratedCollection.objects.order_by('tag')]

def site_dir():
    return settings.SITE_DIR

def handle_exc():
    exc_type, exc_value, exc_traceback = sys.exc_info()
    traceback.print_exception(exc_type, exc_value, exc_traceback,
                              file=sys.stdout)

def find_readme(file_name):
    for x in settings.README_TEMPLATES:
        if x['file'] == file_name:
            return x

def readme_files():
    return [ x['file'] for x in settings.README_TEMPLATES ]

def setup_logger(logger):
    log_format = '%(asctime)s - %(name)-15s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.DEBUG, format=log_format, stream=sys.stdout)
    # ch = logging.StreamHandler(sys.stdout)
    # ch.setLevel(logging.DEBUG)
    # formatter = logging.Formatter('%(asctime)s - %(name)-15s - %(levelname)s - %(message)s')
    # ch.setFormatter(formatter)
    # logging.getLogger().addHandler(ch)
    logger.setLevel(logging.DEBUG)
    # logging.getLogger().setLevel(logging.DEBUG)
    # global logger
    # logger = logging.getLogger(__name__)
    logging.debug("We're debugging!")

def update_online(doc):
    if doc.is_online:
        pass
    else:
        if doc.is_live():
            doc.is_online = True
            doc.save()
        logging.info("Is document online? %-15s %-20s %s" % (
            doc.repository.tag, doc.base_dir, str(doc.is_online)))


def update_online_statuses():
    for doc in opfunc.queryset_iterator(Document.objects.all()):
        update_online(doc)
        # if doc.is_online:
        #     pass
        # else:
        #     if doc.is_live():
        #         doc.is_online = True
        #         doc.save()
        # logging.info("Is document online? %-15s %-20s %s" % (
        #     doc.repository.tag, doc.base_dir, str(doc.is_online)))

def is_makeable(page, opts):
    make_page = False

    if page.is_makeable() and (page.is_needed() or opts.force):
        make_page = True
    elif opts.reallyforce:
        make_page = True

    return make_page

def make_browse_html(docid, opts):
    doc = Document.objects.get(pk=docid)
    update_online(doc)
    repo_tag = doc.repository.tag
    repo_wrapper = get_repo_wrapper(repo_tag)
    page = Browse(document=doc, repository_wrapper=repo_wrapper,
                  toc_dir=settings.TOC_DIR,
                  **{'outdir': site_dir()})

    if is_makeable(page, opts):
        logging.info("Creating page: %s" % (page.outfile_path(), ))
        if not opts.dry_run:
            page.create_pages()
    else:
        logging.info("Skipping page: %s" % (page.outfile_path(), ))

def make_toc_html(repowrap, opts):
    page = TableOfContents(
        repowrap, toc_dir=settings.TOC_DIR,
        **{'template_name': 'TableOfContents.html', 'outdir': site_dir()})

    # TODO: have TOC is_needed() check the include file; fails to make
    #       now b/c TableOfContents.html seldom changes
    # For now, always force, and make them all:
    opts.force = True

    if is_makeable(page, opts):
        logging.info("Creating TOC for repository %s: %s" % (
            repowrap.tag(), page.outfile_path()))
        if not opts.dry_run:
            page.create_pages()
    else:
        logging.info("Skipping TOC for repository %s: %s" % (
            repowrap.tag(), page.outfile_path()))

def make_curated_collections_html(opts):
    """ Do the actual work """

    try:
        page = CuratedCollections(settings.CURATED_COLLECTIONS_TEMPLATE,
            site_dir(), toc_dir=settings.TOC_DIR)

        if is_makeable(page, opts):
            logging.info("Creating list of curated collections: %s" % (page.outfile_path(), ))
            if not opts.dry_run:
                page.create_pages()
        else:
            logging.info("Skipping page: %s" % (page.outfile_path(), ))
    except TemplateDoesNotExist as ex:
        msg = "Could not find template: %s" % (settings.CURATED_COLLECTIONS_TEMPLATE,)
        raise OPennException(msg)



def make_readme_html(readme, opts):
    try:
        readme_dict = find_readme(readme)
        if readme_dict == None:
            raise OPennException("Unknown readme file: %s" % (readme,))
        page = Page(readme, site_dir(), title=readme_dict['title'])

        if is_makeable(page, opts):
            logging.info("Creating page: %s" % (page.outfile_path(), ))
            if not opts.dry_run:
                page.create_pages()
        else:
            logging.info("Skipping page: %s" % (page.outfile_path(), ))
    except TemplateDoesNotExist as ex:
        msg = "Could not find template: %s" % (readme,)
        raise OPennException(msg)

def make_repositories(opts):
    try:
        page = Repositories(settings.REPOSITORIES_TEMPLATE, site_dir(),
                           repository_configs(), toc_dir=settings.TOC_DIR)

        if is_makeable(page, opts):
            logging.info("Creating list of repositories: %s" % (page.outfile_path(), ))
            if not opts.dry_run:
                page.create_pages()
        else:
            logging.info("Skipping page: %s" % (page.outfile_path(), ))
    except TemplateDoesNotExist as ex:
        msg = "Could not find template: %s" % (settings.REPOSITORIES_TEMPLATE,)
        raise OPennException(msg)

def make_repositories_csv(opts):
    """Generate repositories.csv file listing all repositories and curated collections.
    """

    csv = CollectionsCSV(outdir=site_dir(), repo_configs=repository_configs())
    if is_makeable(csv, opts):
        if not opts.dry_run:
           csv.write_file()
        logging.info("Wrote repositories CSV file: %s" % (csv.outpath(),))
    else:
        logging.info("Skipping page: %s" % (csv.outfile_path(),))

def make_repository_toc_csv(repo_tag, opts):
    """
    Generate CSV Table of Contents for repository with tag ``repo_tag``.
    """
    repo_wrapper = repository_configs().get_repository(repo_tag)
    csv          = TableOfContentsCSV(repository=repo_wrapper, outdir=site_dir())

    if is_makeable(csv, opts):
        if not opts.dry_run:
            csv.write_file()
        logging.info("Wrote table of contents CSV file: %s" % (csv.outfile_path(),))
    else:
        logging.info("Skipping CSV: %s" % (csv.outfile_path(), ))

def make_curated_toc_csv(curated_tag, opts):
    """
    Generate CSV Table of Contents for curated collections with tag
    ``curated_tag``.
    """
    csv = CuratedCollectionContentsCSV(curated_tag=curated_tag, outdir=site_dir())
    if is_makeable(csv, opts):
        if not opts.dry_run:
            csv.write_file()
        logging.info("Wrote curated collection table of contents CSV file: %s", csv.outfile_path())
    else:
        logging.info("Skipping CSV: %s", csv.outfile_path())

def make_curated_toc_html(curated_tag, opts):
    page = CuratedCollectionTOC(curated_tag=curated_tag, toc_dir=settings.TOC_DIR,
                                **{'template_name': 'CuratedCollectionTOC.html',
                                   'outdir': site_dir()})

    opts.force = True

    if is_makeable(page, opts):
        if not opts.dry_run:
            page.create_pages()
        logging.info("Wrote curated collection HTML table of contents file: %s" % (page.outfile_path(),))
    else:
        logging.info("Skipping curated collection HTML table of contents file: %s" % (page.outfile_path(), ))

# ------------------------------------------------------------------------------
# ACTIONS
# ------------------------------------------------------------------------------
def process_all(opts):
    """Default behavior, process all file types."""
    browse(opts)
    toc(opts)
    repositories_html(opts)
    curated_collections_html(opts)
    readme(opts)
    csv_toc(opts)
    repositories_csv(opts)
    html_toc_all_curated_colls(opts)
    csv_toc_all_curated_collections(opts)

def browse(opts):
    """Generate browse HTML files as needed"""
    # update online statuses of the Documents first
    update_online_statuses()
    docids = [doc.id for doc in opfunc.queryset_iterator(
        Document.objects.filter(is_online = True))]
    for docid in docids:
        try:
            document(docid, opts)
        except OPennException:
            pass

def repositories_html(opts):
    """ Generate Repositories.html """
    make_repositories(opts)

def curated_collections_html(opts):
    """ Generate CuratedCollections.html """
    make_curated_collections_html(opts)

def toc(opts):
    """Generate TOC HTML files as needed"""
    for tag in opfunc.get_repo_tags():
        toc_repository(tag, opts)

def toc_repository(repo_tag, opts):
    """Generate table of contents for repo_tag"""
    repo_wrapper = opfunc.get_repo_wrapper(repo_tag)
    make_toc_html(repo_wrapper, opts)

def document(docid, opts):
    """Generate browse HTML for DOC_ID"""
    try:
        make_browse_html(docid, opts)
    except Exception:
        logging.error("Error processing document with ID %s", str(docid))
        raise

def readme(opts):
    """Generate ReadMe files as needed"""
    for template in settings.README_TEMPLATES:
        readme_file(template['file'], opts)

def readme_file(filename, opts):
    """Generate ReadMe HTML for filename"""
    make_readme_html(filename, opts)

def repositories_csv(opts):
    """Generate repositories CSV"""
    make_repositories_csv(opts)

def csv_toc(opts):
    """Generate CSV table of contents for all repositories.
    """
    for tag in opfunc.get_repo_tags():
        csv_toc_repository(tag, opts)

def csv_toc_repository(repo_tag, opts):
    """Generate CSV table of contents for all repositories"""
    make_repository_toc_csv(repo_tag, opts)

def csv_toc_curated_collection(curated_tag, opts):
    """Generate CSV table of contents for curated_tag"""
    make_curated_toc_csv(curated_tag, opts)

def csv_toc_all_curated_collections(opts):
    """Generate CSV table of contents for all curated collections."""
    for tag in curated_tags():
        make_curated_toc_csv(tag, opts)

def html_toc_curated_collection(curated_tag, opts):
    """ Generate HtML table of contents for curated_tag """
    make_curated_toc_html(curated_tag, opts)

def html_toc_all_curated_colls(opts):
    """ Generate HTML table of contents for all curated collections. """
    for tag in curated_tags():
        html_toc_curated_collection(tag, opts)

def detailed_help(opts):
    """Print detailed help message"""
    print """
%prog [OPTIONS]

Create and stage HTML pages for OPenn.

By default all HTML page types will be generated and staged as needed in this
order:

    1. browse pages for each document on-line
    2. table of contents for each repository with documents on-line
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

A table of contents (TOC) file is generated for any repository that has
documents with published images and browse pages.  A repository's TOC file is
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
include the SITE_DIR, the local directory where pages are staged for pushing
to OPenn; and repository-specific files and subdirectories as defined under
REPOSITORIES[<COLLECTION_KEY>]:

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

Table of contents (TOC) files are created at the repository level.  Each TOC
file lists all published documents for a given repository.  A repository's TOC
file is *makeable" only if there is an HTML browse page for at least one of the
repository's documents.  Note that TOC generation must be run after browse page
generation to be up-to-date.  A TOC file is *needed* if it is makeable and (a) it
hasn't already been staged, or (b) if the currently staged file is older than
at least one of the staged browse HTML for the TOC file's repository.

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
    """.replace('%prog', cmd())

def print_options(opts):
    for k in vars(opts):
        print "OPTION: %33s  %s" % (k, getattr(opts, k))


def check_options(opts):
    # get the options
    opt_dict = copy.deepcopy(vars(opts))

    removal_keys = ['dry_run', 'force', 'reallyforce', 'show_options', 'verbose']

    removed_vals = {}
    for key in removal_keys:
        removed_vals[key] = opt_dict[key]
        del opt_dict[key]

    # # remove dry-run
    # dry_run = opt_dict['dry_run']
    # opt_dict['dry_run'] = False
    # # remove force
    # force = opt_dict['force']
    # opt_dict['force'] = False
    # # remove reallyforce
    # reallyforce = opt_dict['reallyforce']
    # opt_dict['reallyforce'] = False
    # # remove show-options
    # show_options = opt_dict['show_options']
    # opt_dict['show_options'] = False
    # # remove verbose
    # verbose = opt_dict['verbose']
    # opt_dict['verbose'] = False

    # collect used options
    temp_os = dict((k,opt_dict[k]) for k in opt_dict if opt_dict[k])

    if len(temp_os) > 1:
        s = ', '.join(["%s=%s" % (k,str(v)) for k,v in temp_os.iteritems()])
        raise OPennException("More than one option selected: %s" % (s,))

    temp_os = temp_os.update(removed_vals)
    # temp_os['dry_run'] = dry_run
    # temp_os['force'] = force
    # temp_os['show_options'] = show_options
    # temp_os['verbose'] = verbose

    return temp_os

def main(cmdline=None):
    """op-pages

    """
    status = 0
    parser = make_parser()

    opts, args = parser.parse_args(cmdline)
    if opts.show_options:
        print_options(opts)

    # logger = logging.getLogger(__name__)
    # setup_logger(logger)
    log_format = '%(asctime)s - %(name)-15s - %(levelname)s - %(message)s'
    log_level = logging.DEBUG if opts.verbose else logging.INFO
    logging.basicConfig(level=log_level, format=log_format, stream=sys.stdout)
    # logger.setLevel(logging.DEBUG)
    logger.debug("We're debugging!")

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

        elif opts.repository_tag:
            toc_repository(opts.repository_tag, opts)

        elif opts.repositories_html:
            repositories_html(opts)

        elif opts.curated_collections_html:
            curated_collections_html(opts)

        elif opts.document:
            document(opts.document, opts)

        elif opts.readme_file:
            readme_file(opts.readme_file, opts)

        elif opts.repositories_csv:
            repositories_csv(opts)

        elif opts.csv_toc:
            csv_toc(opts)

        elif opts.csv_toc_repository_tag is not None:
            csv_toc_repository(opts.csv_toc_repository_tag, opts)

        elif opts.csv_toc_curated_tag is not None:
            csv_toc_curated_collection(opts.csv_toc_curated_tag, opts)

        elif opts.csv_toc_all_curated_collections:
            csv_toc_all_curated_collections(opts)

        elif opts.detailed_help:
            detailed_help(opts)

        elif opts.html_toc_curated_tag is not None:
            html_toc_curated_collection(opts.html_toc_curated_tag, opts)

        elif opts.html_toc_all_curated_colls:
            html_toc_all_curated_colls(opts)

        else:
            process_all(opts)

        if opts.dry_run:
            logging.warn("DRY RUN COMPLETE; displayed actions approximate")

    except OPennException as ex:
        if opts.verbose:
            handle_exc()
            logging.error(str(ex))
        else:
            logging.error(str(ex))
        status = 4
    except CuratedCollection.DoesNotExist as ex:
        logging.error("Unknown curated collection; use 'op-curt list' for a list")
        status = 4
    except Exception as ex:
        if opts.verbose:
            handle_exc()
        else:
            logging.error(str(ex))
        status = 4

    return status

def make_parser():
    """ option parser"""

    usage = """%prog [OPTIONS]

Create and stage HTML pages for OPenn.

By default all HTML page types will be generated and staged as needed in this
order:

    1. browse pages for each document on-line
    2. table of contents for each repository with documents on-line
    3. all ReadMe files

Use options for more granular behavior, to force creation of certain files, or
to do a dry run of the script.

OPTIONS
=======

Except for --dry-run and --force, options may not be combined.

Note that --dry-run may show inaccurate information for TOC files.  An actual
run may create new browse files that would trigger TOC generation.  Dry runs
don't create new or update browse files, so the TOC steps will likely report
skipped TOC creation for files that would be generated for an actual run.
"""

    parser = OptionParser(usage)

    parser.add_option('-H', '--detailed-help',
                      action='store_true', dest='detailed_help', default=False,
                      help='Print detailed help message')

    parser.add_option('-r', '--repositories',
                      action='store_true', dest='repositories_html', default=False,
                      help='Generate Repositories.html')

    parser.add_option('-q', '--curated-colls',
                      action='store_true', dest='curated_collections_html', default=False,
                      help='Generate CuratedCollections.html')

    parser.add_option('-m', '--readme',
                      action='store_true', dest='readme', default=False,
                      help='Generate ReadMe files as needed')
    parser.add_option('-M', '--readme-file', dest='readme_file', default=None,
                      help=("Generate ReadMe HTML for README, one of:\n  %s" % (
                          ', '.join(readme_files()),)),
                      metavar="README")

    parser.add_option('-t', '--toc',
                      action='store_true', dest='toc', default=False,
                      help='Generate repository TOC HTML files as needed')
    parser.add_option('-T', '--toc-repository', dest='repository_tag', default=None,
                      help=("Generate table of contents for REPOSITORY_TAG; one of: %s" % (
                          ', '.join(opfunc.get_repo_tags()),)),
                      metavar="REPOSITORY_TAG")

    parser.add_option('-z', '--toc-all-curated',
                      action='store_true', dest='html_toc_all_curated_colls', default=False,
                      help="Generate HTML table of contents for all curated collections")
    parser.add_option('-Z', '--toc-curated',
                      dest='html_toc_curated_tag', default=None,
                      help=("Generate HtML table of contents for CURATED_TAG, one of: %s" % (
                          ', '.join(curated_tags()),)),
                      metavar="CURATED_TAG")

    parser.add_option('-b', '--browse',
                      action='store_true', dest='browse', default=False,
                      help='Generate browse HTML files as needed')
    parser.add_option('-B', '--document', dest='document', default=None,
                      help="Generate browse HTML for DOC_ID",
                      metavar="DOC_ID")

    parser.add_option('-c', '--collections-csv',
                      action='store_true', dest='repositories_csv', default=False,
                      help='Generate collections.csv')

    parser.add_option('-x', '--csv-toc',
                      action='store_true', dest='csv_toc', default=False,
                      help="Generate CSV table of contents for all repositories")
    parser.add_option('-X', '--csv-toc-repository',
                      dest='csv_toc_repository_tag', default=None,
                      help=("Generate CSV table of contents for REPOSITORY_TAG, one of: %s" % (
                          ', '.join(opfunc.get_repo_tags()),)),
                      metavar="REPOSITORY_TAG")

    parser.add_option('-u', '--csv-toc-all-curated',
                      action='store_true', dest='csv_toc_all_curated_collections', default=False,
                      help="Generate CSV table of contents for all curated collections")
    parser.add_option('-U', '--csv-toc-curated',
                      dest='csv_toc_curated_tag', default=None,
                      help=("Generate CSV table of contents for CURATED_TAG, one of: %s" % (
                          ', '.join(curated_tags()),)),
                      metavar="CURATED_TAG")

    parser.add_option('-o', '--show-options',
                      action='store_true', dest='show_options', default=False,
                      help='Print out the options at runtime')
    parser.add_option('-n', '--dry-run',
                      action='store_true', dest='dry_run', default=False,
                      help='Make no changes; show what would be done')
    parser.add_option('-f', '--force',
                      action='store_true', dest='force', default=False,
                      help='Create all makeable files; not just as needed')
    parser.add_option('--really-force',
                      action='store_true', dest='reallyforce', default=False,
                      help='Create files even if not makeable [only use for testing]')

    parser.add_option('-v', '--verbose', dest='verbose', default=False,
                      action='store_true', help='Print out lots of info, primarily stack traces')

    return parser

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
