#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Script to view and manage OPenn projects. Use this script to list, validate
project configurations in application settings, and update database with
current project configurations.

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
from openn.collections.config_validator import ConfigValidator
from openn.project.updater import Updater
from openn.project.membership_manager import MembershipManager
from openn.project.duplicate_membership import DuplicateMembership

# Map some convenient sort by aliases
SORT_BY_ALIASES = {
    'id': 'proj_id',
    'tag': 'tag',
    'name': 'name',
    'docs': 'doc_count'
}

SKIP_KEYS = "blurb".split()

BULK_DOC_ID_HEADERS = frozenset(('document_id', 'project_tag'))

BULK_DOC_BASEDIR_HEADERS = frozenset(('project_tag', 'document_base_dir', 'collection_tag'))

# Map the CSV column headers to the arguments for
#
#   MembershipManager#add_document(proj_tag, doc_tag, coll_tag=None)
BULK_HEADER_TO_ARG_MAP = {
    'document_id':          'doc_tag',
    'document_base_dir':    'doc_tag',
    'project_tag':          'proj_tag',
    'collection_tag':       'coll_tag',
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
    return settings.PROJECTS['configs']

def get_validations():
    return settings.PROJECTS['validations']

def get_updater():
    configs = get_configs()
    configs.validate()
    return Updater(configs)

def get_tags():
    return [x['tag'] for x in get_configs()]

def get_names():
    return [x['name'] for x in get_configs()]

def project_tags_in_database():
    return [x.tag for x  in Project.objects.only('tag')]

def get_sort_by_field(arg):
    """Return the keyed value for the argument.
    """
    return SORT_BY_ALIASES.get(arg.lower(), arg)

def get_project_detail(config_dict):
    details = { 'tag': config_dict['tag'] }
    try:
        project = Project.objects.get(tag = config_dict['tag'])
        doc_count = ProjectMembership.objects.filter(
            project_id=project.pk).count()
        details.update({'project_id': str(project.pk),
                        'doc_count': doc_count,
                        'name': project.name})
    except Project.DoesNotExist:
        details.update({'project_id': 'NIBD',
                        'doc_count': 0,
                        'name': config['name']})
    return details

def build_bulk_add_args(headers, csv_row_dict):

    """ Return a dict with row params converted to the arguments for
    MembershipManager#add_document(proj_tag, doc_tag, coll_tag=None).

    Example 1
    ---------

    Input:

        { 'project_tag': 'bibliophilly',
          'collection_tag': 'pennmss',
          'document_base_dir': 'mscodex123' }

    Output:

        { 'doc_tag': 'mscodex123',
          'proj_tag': 'bibliophilly',
          'coll_tag': 'pennmss' }


    Example 2
    ---------

    Input:

        {   'project_tag': 'bibliophilly',
            'document_id': '2' }

    Output:

        {   'doc_tag': '2',
            'proj_tag': 'bibliophilly' }

    """

    params = {}
    for hdr in headers:
        key = BULK_HEADER_TO_ARG_MAP[hdr]
        val = csv_row_dict[hdr]
        params[key] = val

    return params

def get_all_project_details():
    do_validate_configuration()
    details = []
    return [get_project_detail(config) for config in get_configs()]

def get_bulk_headers(csvfile):
    with open(csvfile, 'r') as f:
        first_line = f.readline()
    headers = set(first_line.strip().split(','))
    if headers == BULK_DOC_ID_HEADERS or headers == BULK_DOC_BASEDIR_HEADERS:
        return headers
    else:
        msg = "Headers don't match valid values: %s" % (str(headers),)
        raise OPennException(msg)

def update_projects(args):
    # validate the configuration before we do anything
    do_validate_configuration()
    updater = Updater(get_configs())
    updater.update_all()

def validate_configuration(args):
    do_validate_configuration()
    logging.info("Project configurations are valid")

def add_document(args):
    return add_one_document(
        membership_manager=MembershipManager(),
        proj_tag=args.project_tag,
        doc_tag=args.document_tag,
        coll_tag=args.primary_collection)

def bulk_add_documents(args):
    input_file = args.input_file

    if not os.path.exists(input_file):
        logger.error("Could not find INPUT_FILE: %s" % (input_file,))
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

def add_one_document(membership_manager, proj_tag, doc_tag, coll_tag=None):
    params = {
        'proj_tag': proj_tag,
        'doc_tag': doc_tag,
    }
    if coll_tag is not None:
        params['coll_tag'] = coll_tag

    try:
        membership_manager.add_document(**params)
        logger.info("Added document to project %s" % (params,))
    except Document.MultipleObjectsReturned:
        logger.error("Ambiguous document specification; did you try the --primary-collection option?")
        return 1
    except Document.DoesNotExist:
        logger.error("Unknown document; no document found for DOC_ID '%s'" % (str(doc_tag),))
        return 1
    except Project.DoesNotExist:
        logger.error("Unknown project; no project found for '%s'" % (str(proj_tag),))
        return 1

    return 0

def rm_document(args):
    return rm_one_document(
        membership_manager=MembershipManager(),
        proj_tag=args.project_tag,
        doc_tag=args.document_tag,
        coll_tag=args.primary_collection)

def rm_one_document(membership_manager, proj_tag, doc_tag, coll_tag=None):
    params = {
        'proj_tag': proj_tag,
        'doc_tag': doc_tag,
    }
    if coll_tag is not None:
        params['coll_tag'] = coll_tag

    try:
        membership_manager.remove_document(**params)
        logger.info("Removed document '%s' from project '%s'" % (doc_tag, proj_tag))
    except Document.MultipleObjectsReturned:
        logger.error("Ambiguous document specification; did you try the --primary-collection option?")
        return 1
    except Document.DoesNotExist:
        logger.error("Unknown document; no document found for DOC_ID '%s'" % (str(doc_tag),))
        return 1
    except Project.DoesNotExist:
        logger.error("Unknown project; no project found for '%s'" % (str(proj_tag),))
        return 1
    except ProjectMembership.DoesNotExist:
        logger.error("Document not in project; for project '%s' and document '%s'" % (doc_tag, proj_tag))
        return 1

    return 0

def bulk_rm_documents(args):
    input_file = args.input_file

    if not os.path.exists(input_file):
        logger.error("Could not find INPUT_FILE: %s" % (input_file,))
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

def print_list(projects):
    tag_width = len(max(get_tags(), key=len)) + 2
    name_width = len(max(get_names(), key=len))
    fmtstr = "{proj_id:5}  {tag:%d}  {doc_count:9}  {name}" % (tag_width,)
    print fmtstr.format(proj_id="ID", tag="Tag", doc_count="Doc count",
                        name="Project")

    print fmtstr.format(proj_id="====", tag=("=" * tag_width),
                        doc_count="=========", name=("=" * name_width))
    for proj in projects:
        print_proj(proj, fmtstr, tag_width)

def print_proj(project, fmtstr, tag_width):
    print fmtstr.format(proj_id=project['project_id'], tag=project['tag'],
                               width=tag_width, doc_count=project['doc_count'],
                               name=project['name'])

def list_projects(args):
    configs = get_configs()
    do_validate_configuration()
    details = get_all_project_details()
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
    """op-coll option parser"""

    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)

    subparsers = parser.add_subparsers(help="%(prog)s actions")

    #-----------
    # LIST
    #-----------
    list_help = "List projects and their documents."
    list_description= """List projects and the documents in them.

With no arguments, list projects."""

    list_parser = subparsers.add_parser('list',
        help=list_help,
        description=list_description,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    list_parser.set_defaults(func=list_projects)
    sort_by_help = """ Sort projects by %(metavar)s; options: tag,
        name[the default], proj_id (or id)."""
    list_parser.add_argument('-s', '--sort-by', type=str, default='name',
                                metavar='FIELD', help=sort_by_help)

    #-----------
    # UPDATE
    #-----------
    update_help = "Update projects based on application configuration."
    update_description= """Update projects based on application configuration.

Use `update` to update the database to current values in the settings file.

"""
    update_parser = subparsers.add_parser('update',
        help=update_help,
        description=update_description,
        formatter_class=argparse.RawDescriptionHelpFormatter)

    update_parser.add_argument('-n', '--dry-run', action='store_true', help="Dry-run; show changes to be made.")

    update_parser.set_defaults(func=update_projects)

    #-----------
    # VALIDATE
    #-----------
    validate_help = "Validate the project configuration."
    validate_description= """Validate the project configuration.

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
    add_doc_help ="Add documents to a project."
    add_doc_description = """Add a document to a project.

Project tags
---
%s

Run 'op-coll list' for collection tags.
    """ % ('\n'.join(sorted(project_tags_in_database())),)

    add_doc_parser = subparsers.add_parser('add-doc',
        help=add_doc_help,
        description=add_doc_description,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    add_doc_parser.add_argument('project_tag', metavar='PROJECT_TAG',
        help="add document to project with tag %(metavar)s")
    add_doc_parser.add_argument('document_tag', metavar='DOCUMENT_ID',
        help="add document with ID or basedir %(metavar)s")
    add_doc_parser.add_argument('-c', '--primary-collection',
        type=str, metavar='COLLECTION',
        help="""use document from primary collection with tag %(metavar)s;
                    required if ambiguous basedir is used for DOCUMENT_ID""")
    add_doc_parser.set_defaults(func=add_document)

    #-----------
    # RM-DOC
    #-----------
    rm_doc_help ="Remove documents from a project."
    rm_doc_description = """Remove a document from a project.

Project tags
---
%s

Run 'op-coll list' for collection tags.
    """ % ('\n'.join(sorted(project_tags_in_database())),)

    rm_doc_parser = subparsers.add_parser('rm-doc',
        help=rm_doc_help,
        description=rm_doc_description,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    rm_doc_parser.add_argument('project_tag', metavar='PROJECT_TAG',
        help="remove document from project with tag %(metavar)s")
    rm_doc_parser.add_argument('document_tag', metavar='DOCUMENT_ID',
        help="remove document with ID or basedir %(metavar)s")
    rm_doc_parser.add_argument('-c', '--primary-collection',
        type=str, metavar='COLLECTION',
        help="""use document from primary collection with tag %(metavar)s;
                    required if ambiguous basedir is used for DOCUMENT_ID""")
    rm_doc_parser.set_defaults(func=rm_document)

    #-----------
    # BULK-ADD
    #-----------
    bulk_add_help ="Bulk add documents to projects from a CSV file."
    bulk_add_description = """Bulk add documents from a CSV file.

CSV input file MUST have these columns, either:

(1) project_tag, document_id
(2) project_tag, document_base_dir, collection_tag

First row of CSV file MUST be column names.

Project tags
---
%s

Run 'op-coll list' for collection tags.
    """ % ('\n'.join(sorted(project_tags_in_database())),)

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
    bulk_rm_help ="Bulk remove documents from projects using a CSV file."
    bulk_rm_description = """Bulk remove documents using a CSV file.

CSV input file MUST have these columns, either:

(1) project_tag, document_id
(2) project_tag, document_base_dir, collection_tag

First row of CSV file MUST be column names.

Project tags
---
%s

Run 'op-coll list' for collection tags.
    """ % ('\n'.join(sorted(project_tags_in_database())),)

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
