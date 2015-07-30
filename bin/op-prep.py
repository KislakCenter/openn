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
from datetime import datetime
import os
import sys
import logging

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from openn.openn_settings import OPennSettings
from openn.openn_exception import OPennException
from openn.openn_functions import *
# from openn.prep import medren_prep
from openn.prep.common_prep import CommonPrep
from openn.prep.prep_setup import PrepSetup
from openn.prep.package_validation import PackageValidation
from openn.prep.status import Status

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
    global logger
    logger = logging.getLogger(__name__)


def setup_prepstatus(doc):
    # destroy the associate prep if it exists
    if hasattr(doc, 'prepstatus'):
        prepstatus = doc.prepstatus
        prepstatus.delete()
    prepstatus = PrepStatus(document=doc)
    prepstatus.save()
    return prepstatus

def success_status(prepstatus):
    prepstatus.finished  = datetime.now()
    prepstatus.succeeded = True
    prepstatus.save()

def failure_status(prepstatus, ex):
    prepstatus.finished  = datetime.now()
    prepstatus.succeeded = False
    prepstatus.error     = str(ex)
    prepstatus.save()

def get_collection_config(collection):
    config = settings.COLLECTIONS.get(collection.lower(), None)
    if config is None:
        raise OPennException("Configuration not found for collection: '%s'" % collection)
    return config


def get_collection_prep(source_dir, collection, document):
    config = get_collection_config(collection)
    cls = get_class(config['prep_class'])
    kwargs = config.get('prep_class_kwargs', {})
    return cls(source_dir, collection, document, **kwargs)

def fix_perms(source_dir):
    for root, dirs, files in os.walk(source_dir):
        os.chmod(root, 0775)
        for name in files:
            os.chmod(os.path.join(root, name), 0664)

def validate_source_dir(collection, source_dir):
    config = get_collection_config(collection)
    validation_params = config.get('package_validation', None)
    if validation_params is None:
        return
    validator = PackageValidation(**validation_params)
    errors = validator.validate(source_dir)
    if len(errors) > 0:
        msg = 'Invalid package directory: %s' % (source_dir,)
        raise(OPennException('\n'.join([msg] + errors)))

def clean_dir(source_dir, clobber_pattern):
    clobber_re = re.compile(clobber_pattern)
    for root, dirs, files, in os.walk(source_dir):
        for name in files:
            if clobber_re.search(name):
                path = os.path.join(root, name)
                os.remove(path)

def clobber_document(params):
    doc = get_doc(params)
    logger.info(
        "Preparing to clobber document id: %d, collection: %s, base_dir: %s" % (
            doc.id, doc.collection, doc.base_dir))
    if doc.is_online:
        msg = "Clobber requested, but refusing to delete record "
        msg += "for document on-line at: %s" % (doc.package_dir,)
        raise OPennException(msg)
    else:
        s = None
        while s is None:
            s = raw_input("Proceed? (Type: Yes or No): ")
            s = s.strip()
            if s is not None:
                if s.lower() == 'yes':
                    logger.info("OK. Deleting existing document.")
                    doc.delete()
                elif s.lower() == 'no':
                    raise OPennException("User canceled clobber; no changes made")
                else:
                    print "Please enter 'Yes' or 'No'. I don't understand: %r" % (s,)
                    s = None

def fs_prep(source_dir):
    fix_perms(source_dir)
    os.umask(0002)
    if hasattr(settings, 'CLOBBER_PATTERN'):
        clean_dir(source_dir, settings.CLOBBER_PATTERN)

def prep_dir(collection, source_dir):
    status = 0
    try:
        base_dir = os.path.basename(source_dir)
        # mark that prep has begun
        status_txt = os.path.join(source_dir, 'status.txt')
        if not os.path.exists(status_txt):
            Status(source_dir).write_status(Status.PREP_BEGUN)

        setup = PrepSetup()
        doc = setup.prep_document(collection, base_dir)
        prepstatus = setup_prepstatus(doc)
        collection_prep = get_collection_prep(source_dir, collection, doc)
        fs_prep(source_dir)
        collection_prep.prep_dir()
        common_prep = CommonPrep(source_dir, collection, doc)
        common_prep.prep_dir()
        success_status(prepstatus)
    except OPennException as ex:
        # error_no_exit(cmd(), str(ex))
        failure_status(prepstatus, ex)
        status = 4
        parser.error(str(ex))

    return status


def main(cmdline=None):
    """op-prep main
    """
    setup_logger()

    parser = make_parser()

    opts, args = parser.parse_args(cmdline)

    if len(args) != 2:
        parser.error('Wrong number of arguments')

    collection = args[0]
    source_dir = args[1]

    if source_dir.strip().endswith('/'):
        source_dir = source_dir[:-1]

    if not os.path.exists(source_dir):
        parser.error("SOURCE_DIR does not exist: %s" % source_dir)

    validate_source_dir(collection, source_dir)

    base_dir = os.path.basename(source_dir)
    doc_params = { 'base_dir': base_dir, 'collection': collection }

    if doc_exists(doc_params):
        if opts.resume:
            pass
        elif opts.clobber:
            pass
        elif opts.update:
            parser.error('Update function not yet implemented')
        else:
            parser.error("Document already exists with base_dir"
                         " '%s' and collection '%s'" % (base_dir, collection))

    status_txt = os.path.join(source_dir, 'status.txt')
    if opts.resume:
        if os.path.exists(status_txt):
            pass
        else:
            parser.error('Cannot resume prep without expected status file:\n %s' % (status_txt, ))

    if opts.clobber:
        if doc_exists(doc_params):
            try:
                clobber_document(doc_params)
            except OPennException as ex:
                parser.error(str(ex))
        else:
            parser.error('`op-prep --clobber` called for nonexistent document')

    return prep_dir(collection, source_dir)

def make_parser():
    """get_xml option parser"""

    usage = "%prog [OPTIONS] COLLECTION SOURCE_DIR"
    epilog = """
Prepare the given source diretory for OPenn.

Known collections are: %s.

SOURCE_DIR contains a set of document image TIFF files and a file
named bibid.txt which contains the bibid for the given book or
manuscript.

Update: Note that this function has not yet been implemented.

Resume: Resume will fail if the source directory does not have a
`status.txt` file.

Clobber: Use clobber to replace an existing document that did not
prepare correctly the first time. Will fail if document is on-line.

""" % (', '.join(collection_tags(settings)))
    # usage = "%prog COLLECTION SOURCE_DIR"

    parser = OpOptParser(usage=usage,epilog=epilog)
    parser.add_option('-u', '--update',
                      action='store_true', dest='update', default=False,
                      help='update db if doc exists [default: %default]; NOT YET IMPLEMENTED')

    parser.add_option('-r', '--resume',
                      action='store_true', dest='resume', default=False,
                      help='resume processing of document [default: %default]')

    parser.add_option('-x', '--clobber',
                      action='store_true', dest='clobber', default=False,
                      help='if it exists, delete document from database')

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
