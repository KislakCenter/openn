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
        repository_configs=settings.REPOSITORIES,
        prep_context=settings.PREP_CONTEXT)

    return prep_config_factory.create_prep_config(prep_config_tag)

def get_keywords(opts):
    kws = {}
    if opts.keywords is None:
        pass
    else:
        for pair in opts.keywords.split(':'):
            k, v = pair.split('=')
            kws[k] = v

    return kws

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
        output_dir = os.path.join(opts.out_dir, doc.base_dir)
        if os.path.exists(output_dir):
            raise OPennException("Output directory already exists: %s" % (output_dir))
        else:
            os.mkdir(output_dir)
        kwargs = get_keywords(opts)

        OPennPrep().update_tei(output_dir, doc, prep_config, **kwargs)
    except OPennException as ex:
        status = 4
        parser.error(str(ex))

    return status


def make_parser():
    """op-update-tei option parser"""

    usage = "%prog [OPTIONS] PREP_CONFIG DOCUMENT_ID"
    epilog = """

For a package previously completed document with DOCUMENT_ID using
PREP_CONFIG, add new TEI file to a new document base directory, like
'mscodex123' located in OUT_DIR [default:.]; OUTPUT_DIR can be changed with
the '--out-dir' option.

For example, note the following, for a document with ID 4221 and base
directory 'lewis_e_018':

   $ %prog -k xlsx=lewis_e_018_metadata.xlsx flp-bphil 4221

This will create a new directory 'lewis_e_018' in the current directory, as
well as the contained 'data' directory, and the TEI file:

   ./lewis_e_018/data/lewis_e_018_TEI.xml

Note: script will not run if './lewis_e_018' already exists.

For spreadsheet-based TEI, the 'xlsx' keyword must be used:

    $ %prog -k xlsx=path/to/file.xlsx flp-bphil 4732

For Penn in Hand, no keyword arguments are necessary.

"""
    # usage = "%prog COLLECTION SOURCE_DIR"

    parser = OpOptParser(usage=usage,epilog=epilog)
    parser.add_option('-o', '--out-dir', dest='out_dir', default='.',
                      help="Output TEI file to OUT_DIR [default=%default]",
                      metavar="OUT_DIR")
    parser.add_option('-k', '--keywords', dest='keywords',
                      help="""Optional colon-separated name-value pairs as required by TEI update
procedure (e.g. '-k "n1=val1:n2=val two"')""")

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
