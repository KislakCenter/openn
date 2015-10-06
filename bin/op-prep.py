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

  copy master TIFFs (with correct names to destination) to destination
     folder
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
import json
import shutil

sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))
from openn.openn_settings import OPennSettings
from openn.openn_exception import OPennException
from openn.openn_functions import *
# from openn.prep import medren_prep
from openn.prep.common_prep import CommonPrep
from openn.prep.prep_setup import PrepSetup
from openn.prep.package_validation import PackageValidation
from openn.prep.status import Status
from openn.prep.prep_config_factory import PrepConfigFactory
from openn.collections.configs import Configs
from openn.prep.openn_prep import OPennPrep

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "openn.settings")

# Import your models for use in your script
from openn.models import *
# database access functions
from openn import openn_db
from django.core import serializers
from django.conf import settings

class OpOptParser(OptionParser):
    def format_epilog(self, formatter):
        return self.epilog

def cmd():
    return os.path.basename(__file__)

def stage_doc(source_dir, doc):
    staging_dir = os.environ['OPENN_STAGING_DIR']
    coll_folder = doc.openn_collection.long_id()
    dest_dir    = os.path.join(staging_dir, 'Data', coll_folder, doc.base_dir)
    source      = os.path.abspath(source_dir)
    dest        = os.path.abspath(dest_dir)

    if os.path.exists(dest):
        msg = "Deleting previously staged document: %s"
        logger.warning(msg % (dest,))
        shutil.rmtree(dest)

    shutil.move(source, dest)
    logger.info("Document '%s' staged at %s" % (doc.call_number, dest))

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

def collection_configs():
    return Configs(settings.COLLECTIONS)

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

def fix_perms(source_dir):
    for root, dirs, files in os.walk(source_dir):
        os.chmod(root, 0775)
        for name in files:
            os.chmod(os.path.join(root, name), 0664)

def validate_source_dir(prep_method, source_dir):
    validation_params = prep_method.package_validations()

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
    doc = openn_db.get_doc(params)

    if logger.getEffectiveLevel() >= logging.INFO:
        msg = "Preparing to clobber document id: %d,"
        msg += " collection: %s, base_dir: %s"
        logger.info(msg % doc.id, doc.collection, doc.base_dir)

    if doc.is_online:
        msg = "Clobber requested, but refusing to delete record "
        msg += "for document on-line at: %s" % (doc.package_dir,)
        msg = msg
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
                    msg = "User canceled clobber; no changes made"
                    raise OPennException(msg)
                else:
                    msg = "Please enter 'Yes' or 'No'. I don't understand: %r"
                    print msg % (s,)
                    s = None

def prep_source_dir_arg(source_dir):
    if source_dir.strip().endswith('/'):
        source_dir = source_dir[:-1]

    if not os.path.exists(source_dir):
        msg = "SOURCE_DIR does not exist: %s" % source_dir
        raise OPennException(msg)

    return source_dir

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

    setup_logger()

    parser = make_parser()

    opts, args = parser.parse_args(cmdline)

    if len(args) != 2:
        parser.error('Wrong number of arguments')

    try:
        prep_config_tag  = args[0]
        source_dir       = prep_source_dir_arg(args[1])

        prep_config      = get_prep_config(prep_config_tag)
        openn_collection = prep_config.openn_collection()
        prep_method      = prep_config.prep_method()

        validate_source_dir(prep_method, source_dir)

        base_dir         = os.path.basename(source_dir)
        doc_params       = { 'base_dir': base_dir,
                             'openn_collection': openn_collection }

        if openn_db.doc_exists(doc_params):
            if opts.resume:
                pass
            elif opts.clobber:
                pass
            elif opts.update:
                parser.error('Update function not yet implemented')
            else:
                msg = "Document already exists with base_dir"
                msg += " '%s' and primary collection '%s'"
                parser.error(msg % (base_dir, openn_collection))

        status_txt = os.path.join(source_dir, 'status.txt')
        if opts.resume:
            if os.path.exists(status_txt):
                pass
            else:
                msg = 'Cannot resume prep without expected status file:\n %s'
                parser.error(msg % (status_txt, ))

        if opts.clobber:
            if openn_db.doc_exists(doc_params):
                try:
                    clobber_document(doc_params)
                except OPennException as ex:
                    parser.error(str(ex))
            else:
                msg = '`op-prep --clobber` called for nonexistent document'
                parser.error(msg)

        doc = OPennPrep().prep_dir(source_dir, prep_config)
        stage_doc(source_dir, doc)
    except OPennException as ex:
        status = 4
        print_exc()
        parser.error(str(ex))

    return status


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

""" % (', '.join(get_coll_tags()),)
    # usage = "%prog COLLECTION SOURCE_DIR"

    parser = OpOptParser(usage=usage,epilog=epilog)
    update_help = 'update db if doc exists [default: %default]'
    update_help += ' NOT YET IMPLEMENTED'
    parser.add_option('-u', '--update',
                      action='store_true', dest='update', default=False,
                      help=update_help)

    resume_help = 'resume processing of document [default: %default]'
    parser.add_option('-r', '--resume',
                      action='store_true', dest='resume', default=False,
                      help=resume_help)

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
