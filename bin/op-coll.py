#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Script to view and manage OPenn collections. Use this script to
list and update OPenn primary collections, to view collection details,
and to list documents in each collection.

"""

import os
import sys
import argparse
import logging

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "openn.settings")
from openn.models import *
from django.conf import settings

from openn.collections.updater import Updater
from openn.openn_exception import OPennException
from openn.openn_functions import *
from openn.collections.configs import Configs
from openn.collections.details import Details
from openn.collections.lister import Lister

# Map some convenient sort by aliases
SORT_BY_ALIASES = {
    'id': 'collection_id',
    'tag': 'tag',
    'type': 'metadata_type',
    'toc': 'include_file'
}

DETAIL_KEYS = "tag collection_id name metadata_type documents live include_file".split()
SKIP_KEYS = "blurb".split()

DETAIL_PARAMS = {
    'keys': DETAIL_KEYS,
    'skip': SKIP_KEYS,
    'format': "%16s:  %s"
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
    return Configs(settings.COLLECTIONS)

def get_updater():
    configs = get_configs()
    configs.validate()
    return Updater(configs)

def get_sort_by_field(arg):
    try:
        # return the alias or the key argument itself
        return SORT_BY_ALIASES.get(arg.lower(), arg)
    except KeyError:
        raise OPennException("Uknown sort_by option: %s" % arg)

def update_collections(args):
    updater = get_updater()
    tag     = args.tag

    if tag is None or tag.lower() == 'all':
        updater.update_all()
    else:
        updater.update(tag)

def update_collection(tag):
    updater = get_updater()
    updater.update(tag)

def validate_configuration(args):
    configs = get_configs()
    configs.validate()
    logging.info("Collection configurations are valid")

def print_detail(detail, params=DETAIL_PARAMS):
    keys = params['keys']
    skip = params['skip']
    fmt  = params['format']

    print "%s" % (detail['name'],)
    for k in keys:
        print fmt % (k, detail.get(k))

    # print the rest of the keys
    for k in detail.keys():
        if k not in keys and k not in skip:
            print fmt % (k, detail[k])
    print

def print_list(coll):
    # coll_id = coll.get('collection_id', 'NIDB')


    coll.setdefault('collection_id', 'NIDB')
    # print "%(collection_id)s  %-10(tag)s %5(documents)d %(name)s" % coll
    print "%s  %-10s %5d %s" % (coll['collection_id'], coll['tag'], coll['documents'], coll['name'])

def list_collections(args):
    configs = get_configs()
    configs.validate()
    lister = Lister(configs)
    tag = args.tag
    sort_by = get_sort_by_field(args.sort_by)
    for coll in lister.list_all(sort_by):
        print_list(coll)

def collection_details(args):
    configs = get_configs()
    configs.validate()
    details = Details(configs)
    tag = args.tag
    sort_by = get_sort_by_field(args.sort_by)
    if tag is None or tag.lower() == 'all':
        for detail in details.details(sort_by = sort_by):
            print_detail(detail)
    else:
        print_detail(details.get_details(tag))

def main(arguments):
    setup_logger()

    parser = make_parser()

    args = parser.parse_args(arguments)
    try:
        args.func(args)
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
    list_help = "List primary collections and their documents."
    list_description= """List primary collections and the documents in them.

With no arguments, list primary collections; --verbose adds printing
of document counts.

With the TAG argument, list documents in collection with TAG;
--verbose option forces listing of all documents, highlighting those
in collection with TAG.  Special tag 'all' lists all documents and
their collection memberships; --verbose has no effect."""

    list_parser = subparsers.add_parser('list', help=list_help, description=list_description,
                                        formatter_class=argparse.RawDescriptionHelpFormatter)
    list_parser.add_argument('-v', '--verbose', action='store_true', help='Verbose option.')
    tag_help = """List documents in collection with tag %(metavar)s. With verbose
option, list all documents, highlighting those in the collection with
tag %(metavar)s."""

    list_parser.add_argument('tag', metavar='COLL_TAG', nargs='?', help=tag_help)
    list_parser.set_defaults(func=list_collections)
    sort_by_help = "Sort collections by %(metavar)s; options: tag, name[the default], collection_id (or id)."
    list_parser.add_argument('-s', '--sort-by', type=str, default='name',
                                metavar='FIELD', help=sort_by_help)

    #-----------
    # DETAILS
    #-----------
    details_help = "Give primary collection details."
    details_description= """Give primary collection details.

With no arguments, give details for all primary collections.

With the TAG argument, give details for collection with TAG.
"""
    details_parser = subparsers.add_parser('details', help=details_help, description=details_description,
                                        formatter_class=argparse.RawDescriptionHelpFormatter)
    tag_help = """Give details for collection with tag %(metavar)s."""
    details_parser.add_argument('tag', metavar='COLL_TAG', nargs='?', help=tag_help)
    sort_by_help = "Sort details by %(metavar)s; options: tag, name[the default], collection_id (or id)."
    details_parser.add_argument('-s', '--sort-by', type=str, default='name',
                                metavar='FIELD', help=sort_by_help)
    details_parser.set_defaults(func=collection_details)

    #-----------
    # UPDATE
    #-----------
    update_help = "Update collections based on application configuration."
    update_description= """Update collections based on application configuration.

Use `update` to add new collections in the settings file to the
database.

With the TAG argument, update a single collection.

"""
    update_parser = subparsers.add_parser('update', help=update_help, description=update_description,
                                        formatter_class=argparse.RawDescriptionHelpFormatter)
    update_parser.add_argument('-n', '--dry-run', action='store_true', help="Dry-run; show changes to be made.")

    update_parser.add_argument('tag', metavar='COLL_TAG', nargs='?', help=tag_help)
    update_parser.set_defaults(func=update_collections)

    #-----------
    # VALIDATE
    #-----------
    validate_help = "Validate the collection configuration."
    validate_description= """Validate the collection configuration.

Exits silently if the configuration is valid; otherwise, displays
error message(s).  """
    validate_parser = subparsers.add_parser('validate', help=validate_help, description=validate_description,
                                        formatter_class=argparse.RawDescriptionHelpFormatter)
    validate_parser.set_defaults(func=validate_configuration)

    return parser

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
