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
from openn.openn_functions import *
from openn.prep import medren_prep
from openn.prep.common_prep import CommonPrep

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "openn.settings")

# Import your models for use in your script
from openn.models import *
# database access functions
from openn.openn_db import *
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

def get_collection_prep(source_dir, collection, document):
    config = settings.COLLECTIONS.get(collection.lower(), None)
    if config is None:
        raise OPennException("Configuration not found for collection: '%s'" % collection)
    cls = get_class(config['prep_class'])
    return cls(source_dir, collection, document)

def fix_perms(source_dir):
    for root, dirs, files in os.walk(source_dir):
        os.chmod(root, 0775)
        for name in files:
            os.chmod(os.path.join(root, name), 0664)

def clean_dir(source_dir, clobber_pattern):
    clobber_re = re.compile(clobber_pattern)
    for root, dirs, files, in os.walk(source_dir):
        for name in files:
            if clobber_re.search(name):
                path = os.path.join(root, name)
                os.remove(path)

def main(cmdline=None):
    """op-prep main
    """
    status = 0
    parser = make_parser()

    opts, args = parser.parse_args(cmdline)

    if len(args) != 1:
        parser.error('Wrong number of arguments')

    document_id = args[0]

    setup_logger()
    logger = logging.getLogger(__name__)

    try:
        doc = Document.objects.get(id=document_id)
        collection_prep = get_collection_prep(opts.out_dir, doc.collection, doc)
        collection_prep.regen_partial_tei(doc)
        common_prep = CommonPrep(opts.out_dir, doc.collection, doc)
    except OPennException as ex:
        # error_no_exit(cmd(), str(ex))
        status = 4
        parser.error(str(ex))

    return status


def make_parser():
    """op-update-tei option parser"""

    usage = "%prog [OPTIONS] DOCUMENT_ID"
    epilog = """

For a previously completed package for DOCUMENT_ID, recreate the TEI
file outputting the TEI to OUTPUT_DIR [default:.].


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
