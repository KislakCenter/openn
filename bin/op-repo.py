#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Script to view and manage OPenn repositories. Use this script to list and
update OPenn primary repositories, to view repository details, and to list
documents in each repository.

"""

import os
import sys
import argparse
import logging

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "openn.settings")
from openn.models import *
from django.conf import settings

from openn.repository.updater import Updater
from openn.openn_exception import OPennException
from openn.openn_functions import *
from openn.repository.configs import Configs
from openn.repository.details import Details
from openn.repository.lister import Lister

# Map some convenient sort by aliases
SORT_BY_ALIASES = {
    'id': 'repository_id',
    'tag': 'tag',
    'type': 'metadata_type',
    'toc': 'include_file'
}

DETAIL_KEYS = "tag repository_id name metadata_type documents live include_file".split()
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
    return Configs(settings.REPOSITORIES)

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

def update_repositories(args):
    updater = get_updater()
    tag     = args.tag

    if tag is None or tag.lower() == 'all':
        updater.update_all()
    else:
        updater.update(tag)

def update_repository(tag):
    updater = get_updater()
    updater.update(tag)

def validate_configuration(args):
    configs = get_configs()
    configs.validate()
    logging.info("Repository configurations are valid")

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

def print_repo(repo, fmtstr, tag_width):
    repo.setdefault('repository_id', 'NIDB')
    print fmtstr.format(repo_id=repo['repository_id'], tag=repo['tag'],
                               width=tag_width, doc_count=repo['documents'],
                               name=repo['name'])

def print_list(repos):
    tag_width = len(max(get_repo_tags(), key=len)) + 2
    name_width = len(max(get_repo_names(), key=len))
    fmtstr = "{repo_id:5}  {tag:%d}  {doc_count:9}  {name}" % (tag_width,)
    print fmtstr.format(repo_id="ID", tag="Tag", doc_count="Doc count",
                        name="Repository")

    print fmtstr.format(repo_id="====", tag=("=" * tag_width),
                        doc_count="=========", name=("=" * name_width))
    for repo in repos:
        print_repo(repo, fmtstr, tag_width)


def list_repositories(args):
    configs = get_configs()
    configs.validate()
    lister = Lister(configs)
    tag = args.tag
    sort_by = get_sort_by_field(args.sort_by)
    print_list(lister.list_all(sort_by))

def repository_details(args):
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
    """op-repo option parser"""

    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)

    subparsers = parser.add_subparsers(help="%(prog)s actions")

    #-----------
    # LIST
    #-----------
    list_help = "List primary repositories and their documents."
    list_description= """List primary repositories and the documents in them.

With no arguments, list primary repositories; --verbose adds printing
of document counts.

With the TAG argument, list documents in repository with TAG;
--verbose option forces listing of all documents, highlighting those
in repository with TAG.  Special tag 'all' lists all documents and
their repository memberships; --verbose has no effect."""

    list_parser = subparsers.add_parser('list', help=list_help, description=list_description,
                                        formatter_class=argparse.RawDescriptionHelpFormatter)
    list_parser.add_argument('-v', '--verbose', action='store_true', help='Verbose option.')
    tag_help = """List documents in repository with tag %(metavar)s. With verbose
option, list all documents, highlighting those in the repository with
tag %(metavar)s."""

    list_parser.add_argument('tag', metavar='REPO_TAG', nargs='?', help=tag_help)
    list_parser.set_defaults(func=list_repositories)
    sort_by_help = "Sort repositories by %(metavar)s; options: tag, name[the default], repository_id (or id)."
    list_parser.add_argument('-s', '--sort-by', type=str, default='name',
                                metavar='FIELD', help=sort_by_help)

    #-----------
    # DETAILS
    #-----------
    details_help = "Give primary repository details."
    details_description= """Give primary repository details.

With no arguments, give details for all primary repositories.

With the TAG argument, give details for repository with TAG.
"""
    details_parser = subparsers.add_parser('details', help=details_help, description=details_description,
                                        formatter_class=argparse.RawDescriptionHelpFormatter)
    tag_help = """Give details for repository with tag %(metavar)s."""
    details_parser.add_argument('tag', metavar='REPO_TAG', nargs='?', help=tag_help)
    sort_by_help = "Sort details by %(metavar)s; options: tag, name[the default], repository_id (or id)."
    details_parser.add_argument('-s', '--sort-by', type=str, default='name',
                                metavar='FIELD', help=sort_by_help)
    details_parser.set_defaults(func=repository_details)

    #-----------
    # UPDATE
    #-----------
    update_help = "Update repositories based on application configuration."
    update_description= """Update repositories based on application configuration.

Use `update` to add new repositories in the settings file to the
database.

With the TAG argument, update a single repository.

"""
    update_parser = subparsers.add_parser('update', help=update_help, description=update_description,
                                        formatter_class=argparse.RawDescriptionHelpFormatter)
    update_parser.add_argument('-n', '--dry-run', action='store_true', help="Dry-run; show changes to be made.")

    update_parser.add_argument('tag', metavar='REPO_TAG', nargs='?', help=tag_help)
    update_parser.set_defaults(func=update_repositories)

    #-----------
    # VALIDATE
    #-----------
    validate_help = "Validate the repository configuration."
    validate_description= """Validate the repository configuration.

Exits silently if the configuration is valid; otherwise, displays
error message(s).  """
    validate_parser = subparsers.add_parser('validate', help=validate_help, description=validate_description,
                                        formatter_class=argparse.RawDescriptionHelpFormatter)
    validate_parser.set_defaults(func=validate_configuration)

    return parser

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
