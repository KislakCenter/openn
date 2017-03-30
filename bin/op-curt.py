#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Script to view and manage OPenn curated collections. Use this script to
list, validate curated collection configurations in application settings, and
update database with current curated collection configurations.

"""

import os
import sys
import csv
import argparse
import logging

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "openn.settings")
from openn.models import *
from django.conf import settings

from openn.openn_exception import OPennException
import openn.openn_functions as opfunc
from openn.openn_functions import *
from openn.repository.config_validator import ConfigValidator
from openn.curated.updater import Updater
from openn.curated.membership_manager import MembershipManager
from openn.curated.duplicate_membership import DuplicateMembership

# Map some convenient sort by aliases
SORT_BY_ALIASES = {
    'id': 'curated_id',
    'tag': 'tag',
    'name': 'name',
    'docs': 'doc_count'
}

SKIP_KEYS = "blurb".split()

BULK_DOC_ID_HEADERS = frozenset(('document_id', 'curated_collection_tag'))

BULK_DOC_BASEDIR_HEADERS = frozenset(('curated_collection_tag', 'document_base_dir', 'repository_tag'))

# Map the CSV column headers to the arguments for
#
#   MembershipManager#add_document(curated_tag, doc_tag, repo_tag=None)
BULK_HEADER_TO_ARG_MAP = {
    'document_id':            'doc_tag',
    'document_base_dir':      'doc_tag',
    'curated_collection_tag': 'curated_tag',
    'repository_tag':         'repo_tag',
}

def setup_logger():
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)-15s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    logging.getLogger().addHandler(ch)
    logging.getLogger().setLevel(logging.DEBUG)
    global logger
    logger = logging.getLogger(__name__)

def get_configs():
    return settings.CURATED_COLLECTIONS['configs']

def get_validations():
    return settings.CURATED_COLLECTIONS['validations']

def get_updater():
    configs = get_configs()
    configs.validate()
    return Updater(configs)

def get_tags():
    return [x['tag'] for x in get_configs()]

def get_names():
    return [x['name'] for x in get_configs()]

def curated_collection_tags_in_database():
    return [x.tag for x  in CuratedCollection.objects.only('tag')]

def get_sort_by_field(arg):
    """Return the keyed value for the argument.
    """
    return SORT_BY_ALIASES.get(arg.lower(), arg)

def get_curated_collection_detail(config_dict):
    details = { 'tag': config_dict['tag'] }
    try:
        curated = CuratedCollection.objects.get(tag = config_dict['tag'])
        doc_count = CuratedMembership.objects.filter(
            curated_collection_id=curated.pk).count()
        details.update({'curated_collection_id': str(curated.pk),
                        'doc_count': doc_count,
                        'name': curated.name})
    except CuratedCollection.DoesNotExist:
        details.update({'curated_collection_id': 'NIBD',
                        'doc_count': 0,
                        'name': config['name']})
    return details

def build_bulk_add_args(headers, csv_row_dict):

    """ Return a dict with row params converted to the arguments for
    MembershipManager#add_document(curated_tag, doc_tag, repo_tag=None).

    Example 1
    ---------

    Input:

        { 'curated_collection_tag': 'bibliophilly',
          'repository_tag': 'pennmss',
          'document_base_dir': 'mscodex123' }

    Output:

        { 'doc_tag': 'mscodex123',
          'curated_tag': 'bibliophilly',
          'repo_tag': 'pennmss' }


    Example 2
    ---------

    Input:

        {   'curated_collection_tag': 'bibliophilly',
            'document_id': '2' }

    Output:

        {   'doc_tag': '2',
            'curated_tag': 'bibliophilly' }

    """

    params = {}
    for hdr in headers:
        key = BULK_HEADER_TO_ARG_MAP[hdr]
        val = csv_row_dict[hdr]
        params[key] = val

    return params

def get_all_curated_collection_details():
    do_validate_configuration()
    details = []
    return [get_curated_collection_detail(config) for config in get_configs()]

def get_bulk_headers(csvfile):
    with open(csvfile, 'r') as f:
        first_line = f.readline()
    headers = set(first_line.strip().split(','))
    if headers == BULK_DOC_ID_HEADERS or headers == BULK_DOC_BASEDIR_HEADERS:
        return headers
    else:
        msg = "Headers don't match valid values: %s" % (str(headers),)
        raise OPennException(msg)

def update_curated_collections(args):
    # validate the configuration before we do anything
    do_validate_configuration()
    updater = Updater(get_configs())
    updater.update_all()

def validate_configuration(args):
    do_validate_configuration()
    logging.info("CuratedCollection configurations are valid")

def add_document(args):
    return add_one_document(
        membership_manager=MembershipManager(),
        curated_tag=args.curated_collection_tag,
        doc_tag=args.document_tag,
        repo_tag=args.repository)

def bulk_add_documents(args):
    input_file = args.input_file

    if not os.path.exists(input_file):
        logger.error("Could not find INPUT_FILE: %s", input_file,)
        return 1

    headers = get_bulk_headers(input_file)

    with open(input_file, 'rb') as csvfile:
        rdr = csv.DictReader(csvfile)
        membership_manager = MembershipManager()
        for row in rdr:
            params = build_bulk_add_args(headers,row)
            try:
                add_one_document(membership_manager, **params)
            except DuplicateMembership as dmx:
                logger.error(str(dmx))

def add_one_document(membership_manager, curated_tag, doc_tag, repo_tag=None):
    params = {
        'curated_tag': curated_tag,
        'doc_tag': doc_tag,
    }
    if repo_tag is not None:
        params['repo_tag'] = repo_tag

    try:
        membership_manager.add_document(**params)
        logger.info("Added document to curated collection %s", params,)
    except Document.MultipleObjectsReturned:
        logger.error("Ambiguous document specification; did you try the --repository option?")
        return 1
    except Document.DoesNotExist:
        logger.error("Unknown document; no document found for DOC_ID '%s'", str(doc_tag),)
        return 1
    except CuratedCollection.DoesNotExist:
        logger.error("Unknown curated collection; no curated collection"
                     " found for '%s'", str(curated_tag),)
        return 1

    return 0

def rm_document(args):
    return rm_one_document(
        membership_manager=MembershipManager(),
        curated_tag=args.curated_collection_tag,
        doc_tag=args.document_tag,
        repo_tag=args.repository)

def rm_one_document(membership_manager, curated_tag, doc_tag, repo_tag=None):
    params = {
        'curated_tag': curated_tag,
        'doc_tag': doc_tag,
    }
    if repo_tag is not None:
        params['repo_tag'] = repo_tag

    try:
        membership_manager.remove_document(**params)
        logger.info("Removed document '%s' from curated collection '%s'", doc_tag, curated_tag)
    except Document.MultipleObjectsReturned:
        logger.error("Ambiguous document specification; did you try the --repository option?")
        return 1
    except Document.DoesNotExist:
        logger.error("Unknown document; no document found for DOC_ID '%s'", str(doc_tag),)
        return 1
    except CuratedCollection.DoesNotExist:
        logger.error("Unknown curated collection; no curated collection found"
                     " for '%s'", str(curated_tag),)
        return 1
    except CuratedMembership.DoesNotExist:
        logger.error("Document not in curated collection; for curated collection '%s'"
                     " and document '%s'", doc_tag, curated_tag)
        return 1

    return 0

def bulk_rm_documents(args):
    input_file = args.input_file

    if not os.path.exists(input_file):
        logger.error("Could not find INPUT_FILE: %s", input_file,)
        return 1

    headers = get_bulk_headers(input_file)

    with open(input_file, 'rb') as csvfile:
        rdr = csv.DictReader(csvfile)
        membership_manager = MembershipManager()
        for row in rdr:
            params = build_bulk_add_args(headers,row)
            rm_one_document(membership_manager, **params)

def do_validate_configuration():
    validator = ConfigValidator(get_validations(), get_configs())
    validator.validate()

def print_list(curated_collections):
    tag_width = len(max(get_tags(), key=len)) + 2
    name_width = len(max(get_names(), key=len))
    fmtstr = "{curated_id:5}  {tag:%d}  {doc_count:9}  {name}" % (tag_width,)
    print fmtstr.format(curated_id="ID", tag="Tag", doc_count="Doc count",
                        name="CuratedCollection")

    print fmtstr.format(curated_id="====", tag=("=" * tag_width),
                        doc_count="=========", name=("=" * name_width))
    for curated in curated_collections:
        print_curated(curated, fmtstr, tag_width)

def print_curated(curated_collection, fmtstr, tag_width):
    print fmtstr.format(curated_id=curated_collection['curated_collection_id'],
                        tag=curated_collection['tag'],
                        width=tag_width,
                        doc_count=curated_collection['doc_count'],
                        name=curated_collection['name'])

def list_curated_collections(args):
    configs = get_configs()
    do_validate_configuration()
    details = get_all_curated_collection_details()
    details = sorted(details, key=lambda k: k['tag'])
    print_list(details)

def main(arguments):
    setup_logger()

    parser = make_parser()

    args = parser.parse_args(arguments)
    try:
        return args.func(args)
    except OPennException as ex:
        parser.error(unicode(ex))

def make_parser():
    """op-curt option parser"""

    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)

    subparsers = parser.add_subparsers(help="%(prog)s actions")

    #-----------
    # LIST
    #-----------
    list_help = "List curated collections and their documents."
    list_description= """List curated collections and the documents in them.

With no arguments, list curated collections."""

    list_parser = subparsers.add_parser('list',
        help=list_help,
        description=list_description,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    list_parser.set_defaults(func=list_curated_collections)
    sort_by_help = """ Sort curated collections by %(metavar)s; options: tag,
        name[the default], curated_id (or id)."""
    list_parser.add_argument('-s', '--sort-by', type=str, default='name',
                                metavar='FIELD', help=sort_by_help)

    #-----------
    # UPDATE
    #-----------
    update_help = "Update curated collections based on application configuration."
    update_description= """Update curated collections based on application configuration.

Use `update` to update the database to current values in the settings file.

"""
    update_parser = subparsers.add_parser('update',
        help=update_help,
        description=update_description,
        formatter_class=argparse.RawDescriptionHelpFormatter)

    update_parser.add_argument('-n', '--dry-run', action='store_true', help="Dry-run; show changes to be made.")

    update_parser.set_defaults(func=update_curated_collections)

    #-----------
    # VALIDATE
    #-----------
    validate_help = "Validate the curated collection configuration."
    validate_description= """Validate the curated collection configuration.

Exits silently if the configuration is valid; otherwise, displays
error message(s).  """
    validate_parser = subparsers.add_parser('validate',
        help=validate_help,
        description=validate_description,
        formatter_class=argparse.RawDescriptionHelpFormatter)

    validate_parser.set_defaults(func=validate_configuration)

    #-----------
    # ADD-DOC
    #-----------
    add_doc_help ="Add documents to a curated collection."
    add_doc_description = """Add a document to a curated collection.

CuratedCollection tags
---
%s

Run 'op-repo list' for repository tags.
    """ % ('\n'.join(sorted(curated_collection_tags_in_database())),)

    add_doc_parser = subparsers.add_parser('add-doc',
        help=add_doc_help,
        description=add_doc_description,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    add_doc_parser.add_argument('curated_collection_tag', metavar='CURATED_COLLECTION_TAG',
        help="add document to curated collection with tag %(metavar)s")
    add_doc_parser.add_argument('document_tag', metavar='DOCUMENT_ID',
        help="add document with ID or basedir %(metavar)s")
    add_doc_parser.add_argument('-c', '--repository',
        type=str, metavar='REPOSITORY',
        help="""use document from repository with tag %(metavar)s;
                    required if ambiguous basedir is used for DOCUMENT_ID""")
    add_doc_parser.set_defaults(func=add_document)

    #-----------
    # RM-DOC
    #-----------
    rm_doc_help ="Remove documents from a curated collection."
    rm_doc_description = """Remove a document from a curated collection.

CuratedCollection tags
---
%s

Run 'op-repo list' for repository tags.
    """ % ('\n'.join(sorted(curated_collection_tags_in_database())),)

    rm_doc_parser = subparsers.add_parser('rm-doc',
        help=rm_doc_help,
        description=rm_doc_description,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    rm_doc_parser.add_argument('curated_collection_tag', metavar='CURATED_COLLECTION_TAG',
        help="remove document from curated collection with tag %(metavar)s")
    rm_doc_parser.add_argument('document_tag', metavar='DOCUMENT_ID',
        help="remove document with ID or basedir %(metavar)s")
    rm_doc_parser.add_argument('-c', '--repository',
        type=str, metavar='REPOSITORY',
        help="""use document from repository with tag %(metavar)s;
                    required if ambiguous basedir is used for DOCUMENT_ID""")
    rm_doc_parser.set_defaults(func=rm_document)

    #-----------
    # BULK-ADD
    #-----------
    bulk_add_help ="Bulk add documents to curated collections from a CSV file."
    bulk_add_description = """Bulk add documents from a CSV file.

CSV input file MUST have these columns, either:

(1) curated_collection_tag, document_id
(2) curated_collection_tag, document_base_dir, repository_tag

First row of CSV file MUST be column names.

CuratedCollection tags
---
%s

Run 'op-coll list' for collection tags.
    """ % ('\n'.join(sorted(curated_collection_tags_in_database())),)

    bulk_add_parser = subparsers.add_parser('bulk-add',
        help=bulk_add_help,
        description=bulk_add_description,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    bulk_add_parser.add_argument('input_file', metavar='INPUT_FILE',
        help="add documents listed in CSV file %(metavar)s")
    bulk_add_parser.set_defaults(func=bulk_add_documents)

    #-----------
    # BULK-RM
    #-----------
    bulk_rm_help ="Bulk remove documents from curated collections using a CSV file."
    bulk_rm_description = """Bulk remove documents using a CSV file.

CSV input file MUST have these columns, either:

(1) curated_collection_tag, document_id
(2) curated_collection_tag, document_base_dir, repository_tag

First row of CSV file MUST be column names.

CuratedCollection tags
---
%s

Run 'op-coll list' for collection tags.
    """ % ('\n'.join(sorted(curated_collection_tags_in_database())),)

    bulk_rm_parser = subparsers.add_parser('bulk-rm',
        help=bulk_rm_help,
        description=bulk_rm_description,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    bulk_rm_parser.add_argument('input_file', metavar='INPUT_FILE',
        help="add documents listed in CSV file %(metavar)s")
    bulk_rm_parser.set_defaults(func=bulk_rm_documents)

    return parser

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
