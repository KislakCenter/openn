#!/usr/bin/env python

"""Module summary

-  collect metadata using BibID
-  confirm directory name matches object name
-  extract the file names from the XML
-  compare XML file names with actual file names
-  generate new names using BibID
    - build filename list:
        files from file system in order;
        check list of files in XML
    - build list of filenames with labels

  copy master TIFFs (with correct names to destination) to destination folder
  generate derivatives
  create manifest
  create TEI with new filenames and paths
"""

# optparse is both easy to use and produces clean code
# the main optparse docs can be found here:
# http://docs.python.org/library/optparse.html
# there's a much better tutorial that works you through optparse
# starting with a simple example and slowly adding complexity.
from optparse import OptionParser
import os
import sys
import logging

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from openn.openn_exception import OPennException
from openn.openn_functions import *
from openn.prep import medren_prep
from openn.prep.common_prep import CommonPrep

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "openn.settings")

# Import your models for use in your script
from openn.models import *
from django.core import serializers
from django.conf import settings

def cmd():
    return os.path.basename(__file__)

def setup_logger():
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)-15s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    logging.getLogger().addHandler(ch)
    logging.getLogger().setLevel(logging.DEBUG)

def get_collection_prep(source_dir, collection):
    config = settings.COLLECTIONS.get(collection.lower(), None)
    if config is None:
        raise OPennException("Configuration not found for %s" % collection)
    cls = get_class(config['prep_class'])
    return cls(source_dir, collection)

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

    if len(args) != 2:
        parser.error('Wrong number of arguments')

    collection = args[0]
    source_dir = args[1]

    setup_logger()
    logger = logging.getLogger(__name__)

    collection_prep = get_collection_prep(source_dir, collection)

    try:
        fix_perms(source_dir)
        os.umask(0002)
        if hasattr(settings, 'CLOBBER_PATTERN'):
            clean_dir(source_dir, settings.CLOBBER_PATTERN)
        collection_prep.prep_dir()
        common_prep = CommonPrep(source_dir, collection)
        common_prep.prep_dir()
    except OPennException as ex:
        # error_no_exit(cmd(), str(ex))
        status = 4
        parser.error(str(ex))

    return status


def make_parser():
    """get_xml option parser"""

    usage = """%prog COLLECTION SOURCE_DIR

Prepare the given source diretory for OPenn.

SOURCE_DIR contains a set of manuscript or book image TIFF files, a
sha1manifest.txt file, and a file bibid.txt which contains the bibid for the
given book or manuscript.
"""

    parser = OptionParser(usage)

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
