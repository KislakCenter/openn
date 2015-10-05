#!/usr/bin/env python

"""Module summary

"""

from optparse import OptionParser
import os
import sys
import logging
import codecs

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from openn.openn_exception import OPennException
from openn.prep import medren_prep
from openn.prep.common_prep import CommonPrep

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "openn.settings")
import openn.openn_functions as opfunc

# Import your models for use in your script
from openn.models import *
# database access functions
from openn.openn_db import *
from openn.prep.prep_config_factory import PrepConfigFactory
from openn.prep.openn_prep import OPennPrep
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
    formatter = logging.Formatter('%(asctime)s - %(name)-15s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    logging.getLogger().addHandler(ch)
    logging.getLogger().setLevel(logging.DEBUG)

def get_prep_config(prep_config_tag):
    prep_config_factory = PrepConfigFactory(
        prep_configs_dict=settings.PREP_CONFIGS,
        prep_methods=settings.PREPARATION_METHODS,
        collection_configs=settings.COLLECTIONS,
        prep_context=settings.PREP_CONTEXT)

    return prep_config_factory.create_prep_config(prep_config_tag)

def main(cmdline=None):
    """op-prep main
    """
    status = 0
    parser = make_parser()

    opts, args = parser.parse_args(cmdline)

    if len(args) != 2:
        parser.error('Wrong number of arguments')

    # Prep config is required, b/c only some prep methods implement
    # TEI regeneration.
    prep_config_tag = args[0]
    doc_id          = args[1]

    setup_logger()
    logger = logging.getLogger(__name__)

    try:
        prep_config = get_prep_config(prep_config_tag)
        doc = Document.objects.get(pk=doc_id)

        OPennPrep().update_tei(opts.out_dir, doc, prep_config)
        # collection_prep = get_collection_prep(opts.out_dir, doc.collection, doc)
        # collection_prep.regen_partial_tei(doc)
        # collection_prep._cleanup()

        # # common tei prep
        # common_prep = CommonPrep(opts.out_dir, doc.collection, doc)
        # common_prep.update_tei()
        # common_prep._cleanup()
    except OPennException as ex:
        # error_no_exit(cmd(), str(ex))
        status = 4
        parser.error(str(ex))

    return status


def make_parser():
    """op-update-tei option parser"""

    usage = "%prog [OPTIONS] PREP_CONFIG DOCUMENT_ID"
    epilog = """

For a package previously completed document with DOCUMENT_ID using
PREP_CONFIG, recreate the TEI file outputting the TEI to OUTPUT_DIR
[default:.]; OUTPUT_DIR can be changed with the '--out-dir' option.

NOTE: At present TEI for only PIH (Penn in Hand) documents can be
regenerated.

"""
    # usage = "%prog COLLECTION SOURCE_DIR"

    parser = OpOptParser(usage=usage,epilog=epilog)
    parser.add_option('-o', '--out-dir', dest='out_dir', default='.',
                      help="output TEI file to OUT_DIR [default=%default]",
                      metavar="OUT_DIR")

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
