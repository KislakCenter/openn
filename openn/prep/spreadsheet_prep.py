# -*- coding: utf-8 -*-
import os
import re
import subprocess
import glob
import shutil
import logging
import sys
import codecs
from lxml import etree
from openn.prep.collection_prep import CollectionPrep
from openn.prep.op_workbook import OPWorkbook
from openn.openn_exception import OPennException
from openn.openn_functions import *
from openn.xml.openn_tei import OPennTEI

class SpreadsheetPrep(CollectionPrep):

    logger = logging.getLogger(__name__)

    def __init__(self, source_dir, collection, document, config):
        """
        Create a new SpreadsheetPrep for the given source_dir, collection and document.
        """
        CollectionPrep.__init__(self,source_dir,collection, document)
        self.source_dir_re = re.compile('^%s/*' % source_dir)
        self.data_dir = os.path.join(self.source_dir, 'data')
        self._workbook = None
        self._config = config

    def add_file_list(self,file_list):
        # file_list = self.get_file_list(pih_xml)
        outfile = os.path.join(self.source_dir, 'file_list.json')
        f = open(outfile, 'w')
        f.write(json.dumps(file_list))
        f.close()

    @property
    def xslx_path(self):
        return os.path.join(self.source_dir, 'openn_metadata.xlsx')

    def workbook(self):
        if self._workbook is None:
            self._workbook = OPWorkbook(
                self.xslx_path, self._config)
        return self._workbook

    def validate_workbook(self):
        if not os.path.exists(self.xslx_path):
            msg = 'Cannot find required metadata workbook: %s' % (
                self.xslx_path)
            raise OPennException(msg)

        self.workbook().validate()

    def validate_file_names(self):
        self.workbook().validate_file_lists()

    def build_file_list(self,pih_xml):
        """Build a list of files using the pih_xml file.

        The resulting file list will have the format:

            {
              "document": [
                {
                  "filename": "data/mscodex1589_wk1_front0001.tif",
                  "image_type": "document",
                  "label": "Front cover"
                },
                {
                  "filename": "data/mscodex1589_wk1_front0002.tif",
                  "image_type": "document",
                  "label": "Inside front cover"
                },
                // ...
               ],
              "extra": [
                {
                  "image_type": "extra",
                  "filename": "data/mscodex1589_test ref1_1.tif"
                }
              ]
           }

        The 'document' files will include:

           - all files listed in PIH XML

           - all identifiable 'blank' files; that is, those matching
             the STRICT_IMAGE_PATTERN_RE not found in the PIH list

        """
        expected = self.xml_file_names(pih_xml)
        files = self.prep_file_list(expected)
        xml = etree.parse(open(pih_xml))
        for tif in files.get('document'):
            base         = os.path.splitext(os.path.basename(tif['filename']))[0]
            # //xml[@name = 'pages']/page[@image = 'mscodex1223_wk1_back0001']
            query        = "//xml[@name = 'pages']/page[@image = '%s']" % base
            el           = xml.xpath(query)
            label        = el[0].get('visiblepage') if len(el) > 0 else None
            tif['label'] = self.prep_label(label)
        return files

    def prep_file_list(self, expected):
        """" Create a list of files; only including those listed in the
        workbook.
        """
        files = glob.glob(os.path.join(self.data_dir, '*.tif'))
        files = [ self.source_dir_re.sub('', x) for x in files ]
        sorted_files = sorted(files)
        return { 'document': sorted_files }

    def gen_partial_tei(self):
        raise NotImplementedError

    def regen_partial_tei(self, doc, **kwargs):
        raise NotImplementedError

    def _do_prep_dir(self):
        if self.get_status() > self.COLLECTION_PREP_MD_VALIDATED:
            self.logger.warning("[%s] Metadata alreaady validated" % (self.basedir, ))
        else:
            self.logger.info("[%s] Validating metadata" % (self.basedir, ))
            self.validate_workbook()
            self.write_status(self.COLLECTION_PREP_MD_VALIDATED)

        if self.get_status() > self.COLLECTION_PREP_FILES_VALIDATED:
            self.logger.warning("[%s] Files alreaady validated" % (self.basedir, ))
        else:
            self.logger.info("[%s] Validating files" % (self.basedir, ))
            self.validate_file_names()
            self.write_status(self.COLLECTION_PREP_FILES_VALIDATED)

        if self.get_status() > self.COLLECTION_PREP_FILES_STAGED:
            self.logger.warning("[%s] Files already staged" % (self.basedir, ))
        else:
            self.logger.info("[%s] Staging files" % (self.basedir, ))
            self.fix_image_names()
            self.stage_images()
            self.write_status(self.COLLECTION_PREP_FILES_STAGED)

        if self.get_status() > self.COLLECTION_PREP_FILE_LIST_WRITTEN:
            self.logger.warning("[%s] File list already written" % (self.basedir, ))
        else:
            self.logger.info("[%s] Writing file list" % (self.basedir, ))
            pass
            self.write_status(self.COLLECTION_PREP_FILE_LIST_WRITTEN)

        if self.get_status() > self.COLLECTION_PREP_PARTIAL_TEI_WRITTEN:
            self.logger.warning("[%s] Partial TEI already written" % (self.basedir, ))
        else:
            self.logger.info("[%s] Writing partial TEI" % (self.basedir, ))
            pass
            self.write_status(self.COLLECTION_PREP_PARTIAL_TEI_WRITTEN)

        # files to cleanup
        # TODO: remove workbook ????
