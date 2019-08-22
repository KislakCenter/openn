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

def main(cmdline=None):
    """op-prep main
    """
    status = 0
    parser = make_parser()

    opts, args = parser.parse_args(cmdline)

    if len(args) < 2 or len(args) > 3:
        parser.error('Wrong number of arguments')

    # Prep config is required, b/c only some prep methods implement
    # TEI regeneration.
    prep_config_tag = args[0]
    doc_id          = args[1]
    metadata_dir    = None
    if len(args) > 2:
        metadata_dir = args[2]

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

        kwargs = {}
        if metadata_dir is not None:
            if os.path.exists(metadata_dir):
                kwargs['METADATA_DIR'] = metadata_dir
            else:
                raise OPennException("Cannot find METADATA_DIR: '%s'" % (metadata_dir,))

        OPennPrep().update_tei(output_dir, doc, prep_config, **kwargs)
    except OPennException as ex:
        if opts.verbose:
            opfunc.print_exc()
        status = 4
        parser.error(str(ex))

    return status

def make_parser():
    """op-update-tei option parser"""

    bold = "\033[1m"
    normal_text = "\033[00m"
    usage = "%prog [OPTIONS] PREP_CONFIG DOCUMENT_ID [METADATA_DIR]"
    epilog = """

For a previously completed document with DOCUMENT_ID using PREP_CONFIG, add a
new TEI file to a new document base directory, like 'mscodex123'. METADATA_DIR
contains any files needed by the TEI regeneraration process. Below are
examples for different prep methods and files used from the METADATA_DIR.

By default the new directory is created in the current directory '.', but this
may be changed with the OUT_DIR option.

NOTE: The script will not run if the target directory already exists in
OUT_DIR.

For example, note the following, for a document with ID 4221 and base
directory 'lewis_e_018':

   $ {0} flp-bphil 4221 \
        /mnt/sceti-completed-2/Temporary_sceti-completed/BiblioPhilly/FLP/lewis_e_018

This will create a new directory 'lewis_e_018' in the current directory, copy
the `openn_metadata.xlsx` file from the METADATA_DIR to the new 'lewis_e_018`
and regenerate the TEI file:

   ./lewis_e_018/data/lewis_e_018_TEI.xml

{1}METADATA_DIR PIH FOR PREP METHOD (i.e., pih){2}

METADATA_DIR is not required unless the mansucript has multiple holdings;
however, if BiblioPhilly keywords should be added to the TEI, METADATA_DIR
should be provided and contain `keywords.txt`.

These are those manuscripts for which library systems have descriptive MARC
and structural metadata. Those manuscripts that had SCETI-Admin records or
are now in Colenda with page-level metdata.

Under certain circumstances the METADATA_DIR is required by the application or
the manuscript type.

bibid.txt [ignored]
---
The BibID is taken from the TEI data stored in the database. A
`bibid.txt` file in the METADATA_DIR will be ignored by this script.

holdingid.txt [conditionally required]
---
Conditionally required. For records with more than one holdings record,
METADATA_DIR must be supplied and contain  a `holdingid.txt` file contatining
the correct holdings ID.

keywords.txt [optional; should be used for Penn MedRen mss]
---
If keywords should be added to the TEI (for inclusion in the
BiblioPhilly interface), METADATA_DIR myst be supplied and contain a
`keywords.txt` file.

{1}METADATA_DIR FOR SPREADSHEET PREP METHODS (e.g., diaires, bphil){2}

METADATA_DIR is required.

openn_metadata.xlsx [required]
---
When metadata comes solely from a spreadsheet (diaires and bphil prep
methods), METADATA_DIR must be provided and contain a file name
`openn_metadata.xlsx`.

{1}METADATA_DIR FOR PAGES.XLSX/MARC PREP METHODS (e.g., mmw){2}

METADATA_DIR must be supplied.

METADATA_DIR contents:

bibid.txt [Penn MSS-only, ignored]
---
When relevant, the BibID is taken from the TEI data stored in the database. A
`bibid.txt` file in the METADATA_DIR will be ignored by this script.

holdingid.txt [Penn MSS-only, conditionally required]
---
If a Penn manuscript's MARC record lists more than one holding, this file must
be supplied.

marc.xml [required for non-Penn MSS]
---
Non-Penn manuscripts added by this method must have an accompanying 'marc.xml'
file.

pages.xlsx [required]
---
All manuscripts must have page-level metadata in a 'pages.xlsx' file.

""".format(os.path.basename(sys.argv[0]), bold, normal_text)

    parser = OpOptParser(usage=usage,epilog=epilog)
    parser.add_option('-o', '--out-dir', dest='out_dir', default='.',
                      help="Output TEI file to OUT_DIR [default=%default]",
                      metavar="OUT_DIR")

    parser.add_option('-v', '--verbose', dest='verbose', default=False,
                      action='store_true', help='Print out lots of info, primarily stack traces')

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
