#!/usr/bin/env python

"""op-info

Print out info on object in OP database


"""

import glob
import os
import sys
import logging
from optparse import OptionParser
from datetime import datetime

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "openn.settings")
from openn.models import *
from django.core import serializers
from django.conf import settings

from openn.openn_exception import OPennException
from openn.openn_functions import *
from openn.prep.package_validation import PackageValidation

def cmd():
    return os.path.basename(__file__)

def setup_logger():
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)-15s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    logging.getLogger().addHandler(ch)
    logging.getLogger().setLevel(logging.DEBUG)

def get_validation(coll_name):
    collection = settings.COLLECTIONS.get(coll_name, None)
    if not collection:
        raise(OPennException("Collection not found: %s" % (coll_name,)))
    if collection.get('package_validation', None):
        return PackageValidation(**collection['package_validation'])

def validate(coll_name, pkg_dir):
    errors = []
    validation = get_validation(coll_name)
    if validation:
        errors = validation.validate(pkg_dir)
    else:
        logging.warn("No package_validation configuration found for collection: %s", (coll_name, ))
    return errors

# ------------------------------------------------------------------------------
# ACTIONS
# ------------------------------------------------------------------------------
def main(cmdline=None):
    """op-info

    """
    status = 0
    parser = make_parser()

    opts, args = parser.parse_args(cmdline)

    setup_logger()
    logger = logging.getLogger(__name__)

    try:
        if len(args) != 2:
            raise OPennException("Wrong number of arguments")
        coll_name, pkg_dir = args
        errors = validate(coll_name, pkg_dir)
        if len(errors) > 0:
            logging.error("Errors found checking package directory: %s" % (args[1],))
            for er in errors:
                logging.error(er)
            status = 1
        else:
            logging.info("Valid package directory: %s" % (args[1],))
    except OPennException as ex:
        parser.error(str(ex))
        status = 4
    except Exception as ex:
        parser.error(str(ex))
        status = 4

    return status


def make_parser():
    """ option parser"""

    usage = """%prog COLLECTION PKG_DIR

Check PKG_DIR validity using package_validation rules for COLLECTION.

Package validation rules defined under a collection name in the
settings file:

        COLLECTIONS = {
            'medren': {
                'tag': 'medren',
                'name': 'Penn Manuscripts',
                ...
                'package_validation': {
                    'valid_names': ['*.tif', 'bibid.txt'],
                    'invalid_names': ['CaptureOne', 'Output', '*[()]*'],
                    'required_names': ['*.tif', 'bibid.txt'],
                },
                'config' : {
                    'host': 'dla.library.upenn.edu',
                    ...
                    },
                },
            ...
        }

"""
    parser = OptionParser(usage)

    return parser

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
