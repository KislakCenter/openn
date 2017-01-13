#!/usr/bin/env python

"""Module summary

Usage: op-cust-prep.py REPO_PREP FOLDER_NAME INPUT_FILE

- add the document with FOLDER_NAME using REPO_PREP and the text of
  INPUT_FILE

"""

# optparse is both easy to use and produces clean code
# the main optparse docs can be found here:
# http://docs.python.org/library/optparse.html
# there's a much better tutorial that works you through optparse
# starting with a simple example and slowly adding complexity.
from optparse import OptionParser
from datetime import datetime
import os
import sys
import logging
import shutil

sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "openn.settings")

from openn.openn_exception import OPennException
from openn.prep.prep_setup import PrepSetup
from openn.prep.prep_config_factory import PrepConfigFactory
from openn.repository.configs import Configs


# Import your models for use in your script
from openn.models import *
from openn.openn_functions import *
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

def repository_configs():
    return Configs(settings.REPOSITORIES)

def validate_doc(base_dir, repository, opts):
    params = { 'base_dir': base_dir,
               'repository': repository }
    if openn_db.doc_exists(params):
        if opts.clobber:
            pass
        else:
            msg = "Document already exists with base_dir '%s' "
            msg += "and repository '%s'"
            raise OPennException(msg % (base_dir, repository))
    else:
        if opts.clobber:
            msg = "Clobber option not valid for non-existent document with"
            msg += " base_dir '%s' and repository '%s'"
            raise OPennException(msg % (base_dir, repository))

def setup_prepstatus(doc):
    # destroy the associate prep if it exists
    if hasattr(doc, 'prepstatus'):
        prepstatus = doc.prepstatus
        prepstatus.delete()
    prepstatus = PrepStatus(document=doc)
    prepstatus.save()
    return prepstatus

def set_success_status(prepstatus):
    prepstatus.finished  = datetime.now()
    prepstatus.succeeded = True
    prepstatus.save()

def set_failure_status(prepstatus, ex):
    prepstatus.finished  = datetime.now()
    prepstatus.succeeded = False
    prepstatus.error     = str(ex)
    prepstatus.save()

def get_prep_config(prep_config_tag, folder_name, input_file):
    prep_config_factory = PrepConfigFactory(
        prep_configs_dict=settings.PREP_CONFIGS,
        prep_methods=settings.PREPARATION_METHODS,
        repository_configs=settings.REPOSITORIES,
        prep_context=settings.PREP_CONTEXT)

    return prep_config_factory.create_prep_config(prep_config_tag)

def do_prep(prep_config_tag, folder_name, input_file, opts):
    try:
        prepstatus       = None
        base_dir         = os.path.basename(folder_name)
        prep_config      = get_prep_config(prep_config_tag, folder_name, input_file)
        repository = prep_config.repository()
        validate_doc(base_dir, repository, opts)

        setup            = PrepSetup()
        repo_wrapper     = prep_config.repository_wrapper()
        doc              = setup.prep_document(repo_wrapper, base_dir)

        prepstatus       = setup_prepstatus(doc)

        prep_class       = prep_config.get_prep_class()
        cust_prep        = prep_class(doc, input_file)

        cust_prep.prep()
        set_success_status(prepstatus)
        return doc
    except Exception as ex:
        if prepstatus is not None:
            set_failure_status(prepstatus, ex)
        raise

def main(cmdline=None):
    """op-cust-prep main
    """
    status = 0

    setup_logger()

    parser = make_parser()

    opts, args = parser.parse_args(cmdline)

    if opts.list_repo_preps:
        print "%s" % ('\n'.join(sorted(prep_config_tags())),)
        return status

    if len(args) != 3:
        parser.error('Wrong number of arguments')

    try:
        prep_config_tag  = args[0]
        folder_name      = args[1]
        input_file       = args[2]

        do_prep(prep_config_tag, folder_name, input_file, opts)

    except OPennException as ex:
        status = 4
        print_exc()
        msg = str(ex)
        print msg

    return status


def make_parser():
    """op-cust-prep.py option parser"""

    usage = "%prog [OPTIONS] REPO_PREP FOLDER_NAME INPUT_FILE"
    epilog = """ Prepare FOLDER_NAME as an OPenn document using repository prep
REPO_PREP with descriptive metadata from INPUT_FILE.

Known repository preps are:

    %s

FOLDER_NAME is a path or base directory name to use this document. The
name should correspond to the folder name on OPenn.

Update: Note that this function has not yet been implemented.

Resume: Resume will fail if the source directory does not have a
`status.txt` file.

Clobber: Use clobber to replace an existing document that did not
prepare correctly the first time. Will fail if document is on-line.

""" % ('\n    '.join(sorted(prep_config_tags())),)
    # usage = "%prog COLLECTION SOURCE_DIR"

    parser = OpOptParser(usage=usage,epilog=epilog)

    list_help = 'List all known repository preps and quit; no'
    list_help += ' arguments required; any arguments ignored'
    parser.add_option('-l', '--list',
                      action='store_true', dest='list_repo_preps', default=False,
                      help=list_help)

    clobber_help = 'if it exists, delete document from database'
    parser.add_option('-x', '--clobber',
                      action='store_true', dest='clobber', default=False,
                      help=clobber_help)

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
