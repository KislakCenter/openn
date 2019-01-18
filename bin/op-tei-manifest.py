#!/usr/bin/env python

"""Module summary

"""

from optparse import OptionParser
import os
import sys
import logging
import codecs
import urllib2
import shutil
import hashlib
import re
from distutils import dir_util

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
    global logger
    logger = logging.getLogger(__name__)

def copy_current_manifest(doc, source_dir):
    dest_path = os.path.join(source_dir, 'manifest-sha1.txt')
    if os.path.exists(dest_path):
        logger.info("Manifest found in source_dir: %s", dest_path)
        return

    site_manifest = os.path.join(os.environ['OPENN_SITE_DIR'], doc.manifest_path)
    if os.path.exists(site_manifest):
        logger.info("Copying manifest from %s", site_manifest)
        shutil.copy(site_manifest, source_dir)
        return

    staged_manifest = os.path.join(os.environ['OPENN_STAGING_DIR'], doc.manifest_path)
    if os.path.exists(staged_manifest):
        logger.info("Copying manifest from %s", staged_manifest)
        shutil.copy(staged_manifest, source_dir)
        return

    url = "http://%s/%s" % (settings.OPENN_HOST, doc.manifest_path)
    logger.info("Downloading manifest from %s", url)
    try:
        data = urllib2.urlopen(url).read()
        with open(dest_path, 'w+') as f:
            f.write(data)
    except urllib2.HTTPError as ex:
        if ex.getcode() == 404:
            raise OPennException("Manifest not found at %s" % (url,))
        else:
            raise ex

def rewrite_manifest(doc, source_dir):
    manifest_path  = os.path.join(source_dir, 'manifest-sha1.txt')
    tei_rel_path   = os.path.join('data', doc.tei_basename)
    tei_full_path  = os.path.join(source_dir, tei_rel_path)
    marc_rel_path  = os.path.join('data', 'marc.xml')
    marc_full_path = os.path.join(source_dir, marc_rel_path)

    if not os.path.exists(tei_full_path):
        raise OPennException("No TEI file found at %s" % (tei_full_path,))

    tei_sha1 = hashlib.sha1()
    with open(tei_full_path, 'rb')  as tei:
        tei_sha1.update(tei.read())
    tei_digest = tei_sha1.hexdigest()

    if os.path.exists(marc_full_path):
        marc_sha1 = hashlib.sha1()
        with open(marc_full_path, 'rb') as marc:
            marc_sha1.update(marc.read())
        marc_digest = marc_sha1.hexdigest()

    with open(manifest_path, "r") as manifest:
        lines = manifest.readlines()

    # make sure we need to update the manifest;
    tei_line_re = r'^%s +%s' % (tei_digest, tei_rel_path)
    for line in lines:
        if re.search(tei_line_re, line):
            raise OPennException("Manifest already up-to-date")

    with open(manifest_path, "w") as manifest:
        for line in lines:
            parts = re.split('\s+', line.strip(), 1)
            if len(parts) < 2:
                continue
            file = parts[1]
            if file == tei_rel_path:
                manifest.write("%s  %s\n" % (tei_digest, tei_rel_path))
            elif file == marc_rel_path and marc_digest is not None:
                manifest.write('%s  %s\n"' % (marc_digest, marc_rel_path))
                logger.info('Writing marc_digest: %s' % (marc_digest,))
            else:
                manifest.write(line)

def stage_new(doc, source_dir):
    site_dir = os.path.join(os.environ['OPENN_SITE_DIR'], doc.package_dir)
    if os.path.exists(site_dir):
        logger.info("Found SITE dir; copying %s to %s", source_dir, site_dir)
        print dir_util.copy_tree(source_dir, site_dir)
    else:
        staged_dir = os.path.join(os.environ['OPENN_STAGING_DIR'], doc.package_dir)
        if os.path.exists(staged_dir):
            logger.info("Found STAGED dir; copying %s to %s", source_dir, staged_dir)
        else:
            logger.info("Copying %s to %s", source_dir, staged_dir)
        print dir_util.copy_tree(source_dir, staged_dir)

def update_manifest(doc, source_dir):
    copy_current_manifest(doc, source_dir)
    rewrite_manifest(doc, source_dir)
    stage_new(doc, source_dir)
    logger.info("SUCCESS: TEI and manifest staged for update!")

def cleanup(source_dir, opts):
    if opts.delete_source_dir is False:
        logger.info("NOT Deleting %s", source_dir)
        return

    if opts.delete_source_dir is None:
        delete_dir = raw_input("Delete source directory: %s? [yN] " % (source_dir,))
        if delete_dir.strip().lower() != 'y':
            logger.info("NOT Deleting %s", source_dir)
            return

    logger.info("Deleting %s", source_dir)
    shutil.rmtree(source_dir)

def find_doc(source_dir, opts):
    if opts.doc_id is not None:
        return Document.objects.get(pk=opts.doc_id)

    base_dir = os.path.split(source_dir)[-1]

    if opts.repository is not None:
        repo = Repository.objects.get(tag=opts.repository.lower())
        return Document.objects.get(repository_id=repo.pk, base_dir=base_dir)
    else:
        return Document.objects.get(base_dir=base_dir)

def main(cmdline=None):
    """op-prep main
    """
    status = 0
    parser = make_parser()
    source_dir = None

    opts, args = parser.parse_args(cmdline)


    if len(args) != 1:
        parser.error('Wrong number of arguments')

    source_dir = args[0]

    setup_logger()
    logger = logging.getLogger(__name__)

    if not os.path.exists(source_dir):
        logger.error("Source directory does not exist: %s", source_dir)
        return 1

    try:
        doc = find_doc(source_dir, opts)
        update_manifest(doc, source_dir)
        cleanup(source_dir, opts)
    except Document.MultipleObjectsReturned:
        logger.error("Ambiguous document specification; use --repository or --doc-id option")
        return 1
    except Document.DoesNotExist:
        logger.error("Unknown document; no document found")
        return 1
    except Repository.DoesNotExist:
        logger.error("Unknown repository; no repository"
                     " found for '%s'", str(opts.repository),)

    except OPennException as ex:
        status = 4
        parser.error(str(ex))

    return status


def make_parser():
    """op-update-tei option parser"""

    usage = "%prog [OPTIONS] SOURCE_DIR"
    epilog = """



"""
    # usage = "%prog COLLECTION SOURCE_DIR"

    parser = OpOptParser(usage=usage,epilog=epilog)
    parser.add_option('-r', '--repository', dest='repository', type='string',
                      help="""Provide repo-tag if base_dir extracted from
SOURCE_DIR is ambiguous""")
    parser.add_option('-d', '--doc-id', dest='doc_id', type='int',
                      help="Explicit document ID; overrides other arguments")

    parser.add_option('-x', '--delete-source-dir', dest='delete_source_dir',
                      action="store_true", default=None,
                      help="Remove SOURCE_DIR upone successful completion")

    parser.add_option('-n', '--no-delete-source-dir', dest='delete_source_dir',
                      action="store_false", default=None,
                      help="Leave SOURCE_DIR upone successful completion")

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
