#!/usr/bin/env python

"""Module summary

- Validate a workbook based on the particular repo-prep configuration.

"""

from optparse import OptionParser
import os
import sys
import logging

sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))
from openn.openn_settings import OPennSettings
from openn.openn_exception import OPennException
from openn.openn_functions import *
# from openn.prep import medren_prep
from openn.prep.prep_config_factory import PrepConfigFactory

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "openn.settings")

# database access functions
from openn import openn_db
from django.core import serializers
from django.conf import settings

class OpOptParser(OptionParser):
    def format_epilog(self, formatter):
        return self.epilog

def cmd():
    return os.path.basename(__file__)

def setup_logger():
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.DEBUG)
    fmt = '%(asctime)s - %(name)-15s - %(levelname)s - %(message)s'
    formatter = logging.Formatter(fmt)
    ch.setFormatter(formatter)
    logging.getLogger().addHandler(ch)
    logging.getLogger().setLevel(logging.DEBUG)
    global logger
    logger = logging.getLogger(__name__)

def get_prep_config(prep_config_tag):
    prep_config_factory = PrepConfigFactory(
        prep_configs_dict=settings.PREP_CONFIGS,
        prep_methods=settings.PREPARATION_METHODS,
        repository_configs=settings.REPOSITORIES,
        prep_context=settings.PREP_CONTEXT)

    return prep_config_factory.create_prep_config(prep_config_tag)


def main(cmdline=None):
    """op-prep main
    """
    status = 0

    setup_logger()

    parser = make_parser()

    opts, args = parser.parse_args(cmdline)

    if opts.list_repo_preps:
        print "%s" % ('\n'.join(sorted(prep_config_tags())),)
        return status

    if len(args) != 2:
        parser.error('Wrong number of arguments')

    prep_config_tag  = args[0]
    try:
        print "x"

    except OPennException as ex:
        logger.error(unicode(ex).encode('utf8'))
        status = 4
        if opts.verbose:
            print_exc()

    return status


def make_parser():
    """get_xml option parser"""

    usage = "%prog [OPTIONS] REPO_PREP XLSX_FILE"
    epilog = """
Validate the given XLSX_FILE based on configuration REPO_PREP.

Known repository preps are:

    %s

""" % ('\n    '.join(sorted(prep_config_tags())),)
    # usage = "%prog COLLECTION SOURCE_DIR"

    parser = OpOptParser(usage=usage,epilog=epilog)
    files_help = 'check files listed on the PAGES sheet [default: %default]'
    parser.add_option('-f', '--check-files',
                      action='store_true', dest='check_files', default=False,
                      help=files_help)

    return parser

if __name__ == "__main__":
    # this runs when the application is run from the command
    # it grabs sys.argv[1:] which is everything after the program name
    # and passes it to main
    # the return value from main is then used as the argument to
    # sys.exit, which you can test for in the shell.
    # program exit codes are usually 0 for ok, and non-zero for something
    # going wrong.
    sys.exit(main(sys.argv[1:]))
