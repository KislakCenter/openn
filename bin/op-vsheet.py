#!/usr/bin/env python

"""Module summary

- Validate a workbook based on the particular repo-prep configuration.

"""

from optparse import OptionParser
import os
import sys
import logging
import json

sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))
from openn.openn_settings import OPennSettings
from openn.openn_exception import OPennException
from openn.prep.op_workbook import OPWorkbook
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

def get_config_json(prep_config_tag):
    prep_config = get_prep_config(prep_config_tag)
    config_json = prep_config.prep_class_parameter('config_json')
    return json.load(open(config_json))

def get_workbook(opts, prep_config_tag, workbook_path):
    prep_config = get_prep_config(prep_config_tag)
    config_json = prep_config.prep_class_parameter('config_json')
    config = json.load(open(config_json))
    return OPWorkbook(workbook_path, config)

def validate_description(opts, workbook):
    logger.info("Validating sheet: DESCRIPTION")
    msg = []
    workbook.description.validate()
    if workbook.description.has_errors():
        msg.extend(["Errors found on DESCRIPTION sheet"])
        msg.extend(workbook.description.errors)

    if len(msg) == 0:
        logger.info("OK: No errors in DESCRIPTION sheet!")

    return msg

def print_error_msg(msg_list, workbook_path):
    logger.error('ERRORS FOUND in workbook: %s' % (workbook_path,))
    for msg in msg_list:
        logger.error(msg)

def validate_pages(opts, workbook):
    logger.info("Validating sheet: PAGES")
    msg = []
    workbook.pages.validate()
    if workbook.pages.has_errors():
        msg.extend(["Errors found on PAGES sheet"])
        msg.extend(workbook.pages.errors)

    if len(msg) == 0:
        logger.info("OK: No errors in PAGES sheet!")

    return msg

def validate_workbook(opts, workbook):
    logger.info("Validating workbook: %s", workbook.xlsx_path)
    msg = []

    msg.extend(validate_description(opts, workbook))
    msg.extend(validate_pages(opts, workbook))

    return msg

def validate_files(opts, workbook):
    logger.info("Validating files")
    msg = []

    for sheet in workbook.sheets():
        sheet.validate_file_lists()
        if sheet.has_file_errors():
            msg.extend(["File errors found on sheet %s:" % (sheet.sheet_name.upper(),)])
            msg.extend(sheet.file_errors)

    if len(msg) == 0:
        logger.info("OK: No file errors found!")

    return msg

def run_validation(opts, prep_config_tag, workbook_path):
    msg_list =[]

    workbook = get_workbook(opts, prep_config_tag, workbook_path)
    if opts.check_all:
        msg_list = validate_workbook(opts, workbook)
        msg_list.extend(validate_files(opts, workbook))
    if opts.description:
        msg_list = validate_description(opts, workbook)
    elif opts.pages:
        msg_list = validate_pages(opts, workbook)
    elif opts.files_only:
        msg_list = validate_files(opts, workbook)
    else:
        msg_list = validate_workbook(opts, workbook)

    if not opts.check_all and not opts.files_only and opts.check_files:
        msg_list.extend(validate_files(opts, workbook))

    return msg_list

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
        msg = 'Wrong number of arguments: %d; expected: %d' % (len(args), 2)
        parser.error(msg)

    prep_config_tag  = args[0]
    workbook_path = args[1]
    try:
        msg = []
        msg = run_validation(opts, prep_config_tag, workbook_path)

        if len(msg) > 0:
            print_error_msg(msg, workbook_path)
            status = 1
        else:
            logger.info("SUCCESS! No errrors found.")

    except OPennException as ex:
        logger.error(unicode(ex).encode('utf8'))
        status = 4
        # print_exc()
        # if opts.verbose:
        #     print_exc()

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
    files_help = 'also validate file lists [default: %default]'
    parser.add_option('-f', '--check-files',
                      action='store_true', dest='check_files', default=False,
                      help=files_help)

    files_only_help = 'validate file lists only'
    parser.add_option('-F', '--files-only',
                      action='store_true', dest='files_only', default=False,
                      help=files_only_help)

    list_help = 'list all known repository preps and quit; no'
    list_help += ' arguments required; any arguments ignored'
    parser.add_option('-l', '--list',
                      action='store_true', dest='list_repo_preps', default=False,
                      help=list_help)

    description_help = 'validate DESCRIPTION sheet only'
    parser.add_option('-d', '--description',
                      action='store_true', dest='description', default=False,
                      help=description_help)

    pages_help = 'validate PAGES sheet only'
    parser.add_option('-p', '--pages',
                      action='store_true', dest='pages', default=False,
                      help=pages_help)

    all_help = 'validate PAGES, DESCRIPTION sheets and file lists; other'
    all_help += ' options ignored'
    parser.add_option('-a', '--all',
                      action='store_true', dest='check_all', default=False,
                      help=all_help)

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
