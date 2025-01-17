# -*- coding: utf-8 -*-
import os
import json
import re
import subprocess
import glob
import shutil
import logging
import sys
import codecs
import time
from lxml import etree
from openn.prep.repository_prep import RepositoryPrep
from openn.prep.op_workbook import OPWorkbook
from openn.prep.spreadsheet_xml import SpreadsheetXML
from openn.openn_exception import OPennException
from openn.openn_functions import *
from openn.xml.openn_tei import OPennTEI
from openn.xml.openn_xml import OPennXML

class SpreadsheetPrep(RepositoryPrep):

    SPREADSHEET_OPEN_XML_WRITTEN    = 60
    SPREADSHEET_LICENCE_TYPES_SAVED = 65

    STATUS_NAMES = RepositoryPrep.build_status_names({
        60: 'SPREADSHEET_OPEN_XML_WRITTEN',
        65: 'SPREADSHEET_LICENCE_TYPES_SAVED'
    })

    logger = logging.getLogger(__name__)
    BLANK_RE = re.compile('blank', re.IGNORECASE)
    METADATA_FILES = ['openn_metadata.xlsx']

    def __init__(self, source_dir, document, prep_config):
        """
        Create a new SpreadsheetPrep for the given source_dir, Document, and
        PrepConfig.
        """
        RepositoryPrep.__init__(self,source_dir,document,prep_config)
        self.source_dir_re = re.compile('^%s/*' % source_dir)
        self.data_dir = os.path.join(self.source_dir, 'data')
        self._workbook = None
        self._xsl = prep_config.prep_class_parameter('xsl')
        config_json = prep_config.prep_class_parameter('config_json')
        self._config = json.load(open(config_json))

    def add_file_list(self,file_list):
        # file_list = self.get_file_list(pih_xml)
        outfile = os.path.join(self.source_dir, 'file_list.json')
        with open(outfile, 'w') as f:
            f.write(json.dumps(file_list))
            f.close()

    def openn_xml_path(self):
        return os.path.join(self.source_dir, 'openn_metadata.xml')

    def write_openn_xml(self,outfile):
        if os.path.exists(outfile):
            warning(__name__, 'Removing existing OPenn XML: %s' % (outfile))
            os.remove(outfile)
        with open(outfile, 'w+') as f:

            sp_xml = SpreadsheetXML(self.prep_config.context_var('licences'))
            xml = sp_xml.build_xml(self.workbook().data(), self._config['xml_config'])
            f.write(xml.encode('utf-8'))

    def xml_file_names(self, openn_xml_path):
        names = []
        with open(openn_xml_path) as f:
            tree = etree.parse(f)
            names = tree.xpath('//file_name')
        return [ unicode(x.text, 'utf8') for x in names ]

    def save_rights_data(self, openn_xml_path):
        xml = OPennXML(codecs.open(openn_xml_path, 'r', 'utf-8'))

        if self.prep_config.image_rights() == 'dynamic':
            self.document.image_licence             = xml.image_licence()
            self.document.image_copyright_holder    = xml.image_copyright_holder()
            self.document.image_copyright_year      = xml.image_copyright_year()
            self.document.image_rights_more_info    = xml.image_rights_more_info()
        elif self.prep_config.image_rights().startswith('PD'):
            # TODO: set document.image_licence
            self.document.image_licence = self.prep_config.image_rights()
            self.document.image_copyright_holder = None
            self.document.image_copyright_year = None
            self.document.image_rights_more_info = None
        else:
            # TODO: set document.image_licence
            self.document.image_licence = self.prep_config.image_rights()
            self.document.image_copyright_holder = self.prep_config.rights_holder()
            self.document.image_copyright_year = datetime.now(pytz.UTC).year
            self.document.image_rights_more_info = self.prep_config.rights_more_info()

        if self.prep_config.metadata_rights() == 'dynamic':
            self.document.metadata_licence             = xml.metadata_licence()
            self.document.metadata_copyright_holder    = xml.metadata_copyright_holder()
            self.document.metadata_copyright_year      = xml.metadata_copyright_year()
            self.document.metadata_rights_more_info    = xml.metadata_rights_more_info()
        elif self.prep_config.metadata_rights().startswith('PD'):
            # TODO: set document.metadata_licence
            self.document.metadata_licence = self.prep_config.metadata_rights()
            self.document.metadata_copyright_holder = None
            self.document.metadata_copyright_year = None
            self.document.metadata_rights_more_info = None
        else:
            # TODO: set document.metadata_licence
            self.document.metadata_licence = self.prep_config.metadata_rights()
            self.document.metadata_copyright_holder = self.prep_config.rights_holder()
            self.document.metadata_copyright_year = datetime.now(pytz.UTC).year
            self.document.metadata_rights_more_info = self.prep_config.rights_more_info()

        self.document.save()

    @property
    def xlsx_path(self):
        return os.path.join(self.source_dir, 'openn_metadata.xlsx')

    def workbook(self):
        if self._workbook is None:
            self._workbook = OPWorkbook(
                self.xlsx_path, self._config)
        return self._workbook

    def validate_workbook(self):
        if not os.path.exists(self.xlsx_path):
            msg = 'Cannot find required metadata workbook: %s' % (
                self.xlsx_path)
            raise OPennException(msg)

        self.workbook().validate()

    def validate_file_names(self):
        self.workbook().validate_file_lists()

    def build_file_list(self,openn_xml_path):
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

        expected = [ os.path.join('data', x)
                     for x in self.xml_file_names(openn_xml_path) ]
        files    = self.prep_file_list(expected)
        xml      = etree.parse(open(openn_xml_path))
        for image in files.get('document'):
            base           = os.path.basename(image['filename'])
            query          = "//file_name[text()='%s']/parent::page/display_page" % (base,)
            el             = xml.xpath(query)
            label          = el[0].text if len(el) > 0 else None
            image['label'] = label
            query          = "//file_name[text()='%s']/parent::page/serial_number" % (base,)
            el             = xml.xpath(query)
            serial_number  = el[0].text if len(el) > 0 else None
            image['serial_number'] = serial_number

        return files

    def prep_label(self,label):
        if label is None:
            return 'Unlabeled'
        if self.BLANK_RE.search(label):
            return re.sub(';.*$', '', label)
        else:
            return label

        # files = self.prep_file_list(expected)
        # xml = etree.parse(open(pih_xml))
        # for tif in files.get('document'):
        #     base         = os.path.splitext(os.path.basename(tif['filename']))[0]
        #     # //xml[@name = 'pages']/page[@image = 'mscodex1223_wk1_back0001']
        #     query        = "//xml[@name = 'pages']/page[@image = '%s']" % base
        #     el           = xml.xpath(query)
        #     label        = el[0].get('visiblepage') if len(el) > 0 else None
        #     tif['label'] = self.prep_label(label)
        # return files

    def prep_file_list(self, expected):
        """" Create a list of images files in the directroy. Split the list
        into 'document' and 'extra' files. The 'document' files list
        comprises all those in expected.  The `extra` files list
        consists of all TIFF's that do not match the document image
        patterns.

        """
        all_images = self.image_files(self.data_dir)
        all_images = [ self.source_dir_re.sub('', x) for x in all_images ]
        doc_images = []


        for img in expected:
            if img in all_images:
                all_images.remove(img)
            doc_images.append( { 'filename': img, 'image_type': 'document' } )

        extras = [ { 'filename': x, 'image_type': 'extra', 'label': 'None' } for x in all_images ]

        return { 'document': doc_images, 'extra': extras }

    def gen_partial_tei(self):
        xsl_command = 'op-gen-tei'
        p = subprocess.Popen([xsl_command, self.openn_xml_path(), self._xsl],
                stderr=subprocess.PIPE,
                stdout=subprocess.PIPE)
        out, err = p.communicate()
        if p.returncode != 0:
            raise OPennException("TEI Generation failed: %s" % err)

        return out

    def regen_partial_tei(self, doc, **kwargs):
        xlsx_path = None

        data_dir = kwargs.get('METADATA_DIR', None)

        if data_dir is None:
            msg = 'METADATA_DIR is required to update TEI (document ID: %d)'
            raise OPennException(msg % (self.document.id,))

        # copy the xlsx file into the source_dir as openn_metadata.xlsx
        xlsx_path = os.path.abspath(os.path.join(data_dir, 'openn_metadata.xlsx'))
        dest = os.path.abspath(self.xlsx_path)
        if xlsx_path == dest:
            pass
        else:
            shutil.copyfile(xlsx_path, dest)

        self.write_openn_xml(self.openn_xml_path())
        partial_tei = self.gen_partial_tei()
        # xxxxx
        self.write_partial_tei(self.source_dir, partial_tei)
        self.check_page_count(self.openn_xml_path(), doc)
        self.update_serial_numbers(self.openn_xml_path(), doc)
        self.validate_partial_tei()
        self.archive_xlsx()
        self.add_removal(self.openn_xml_path())
        self.add_removal(self.xlsx_path)

    def update_serial_numbers(self, openn_xml_path, doc):
        xml = OPennXML(codecs.open(openn_xml_path, 'r', 'utf-8'))

        # nothing to do if there are no serial numbers
        if not xml.has_serial_numbers():
            return

        # do nothing if no images
        if doc.image_set.filter(image_type='document').count() == 0:
            return

        # do nothing if we already have serial_number
        first_image = doc.image_set.filter(image_type='document').first()
        if first_image.serial_number is not None:
            return

        images = doc.image_set.filter(image_type='document')
        for page in xml.page_objects():
            base = os.path.basename(str(page.file_name))
            image = [x for x in images if x.filename.endswith(base)][0]
            image.serial_number = page.serial_number
            image.save()

    def check_page_count(self, openn_xml_path, doc):
        """
         Make sure the spreadsheet and the database agree on the number of
         pages; otherwise, we can't proceed.
        """
        xml = OPennXML(codecs.open(openn_xml_path, 'r', 'utf-8'))
        image_count = doc.image_set.filter(image_type='document').count()
        page_count = xml.page_count()
        if page_count != image_count:
            msg = "Spreadsheet page count (%d) does not match document image count (%d)"
            raise OPennException(msg, page_count, image_count)

    def archive_xlsx(self):
        if not os.path.exists(self.xlsx_path):
            return
        repo_wrapper = self.prep_config.repository_wrapper()
        repo_dir = os.path.join(self.prep_config.context_var('archive_dir'),
                                repo_wrapper.folder())
        mkdir_p(repo_dir)

        archive_xlsx = "%s_%s.xlsx" % (self.basedir, tstamptz())
        archive_path = os.path.join(repo_dir, archive_xlsx)
        self.logger.info("[%s] Archiving %s as %s",
            self.basedir, self.xlsx_path, archive_path)
        os.rename(self.xlsx_path, archive_path)

    def _do_prep_dir(self):

        if self.get_status() > self.REPOSITORY_PREP_MD_VALIDATED:
            self.logger.warning("[%s] Metadata alreaady validated", self.basedir, )
        else:
            self.logger.info("[%s] Validating metadata", self.basedir, )
            self.validate_workbook()
            self.write_status(self.REPOSITORY_PREP_MD_VALIDATED)

        if self.get_status() > self.REPOSITORY_PREP_FILES_VALIDATED:
            self.logger.warning("[%s] Files alreaady validated", self.basedir, )
        else:
            self.logger.info("[%s] Validating files", self.basedir, )
            self.validate_file_names()
            self.write_status(self.REPOSITORY_PREP_FILES_VALIDATED)

        if self.get_status() > self.REPOSITORY_PREP_FILES_STAGED:
            self.logger.warning("[%s] Files already staged", self.basedir, )
        else:
            self.logger.info("[%s] Staging files", self.basedir, )
            self.stage_images()
            self.write_status(self.REPOSITORY_PREP_FILES_STAGED)

        if self.get_status() > self.SPREADSHEET_OPEN_XML_WRITTEN:
            self.logger.warning("[%s] OPenn XML already written", self.basedir, )
        else:
            self.logger.info("[%s] Writing OPenn XML", self.basedir, )
            self.write_openn_xml(self.openn_xml_path())
            self.write_status(self.SPREADSHEET_OPEN_XML_WRITTEN)

        if self.get_status() > self.SPREADSHEET_LICENCE_TYPES_SAVED:
            self.logger.warning("[%s] Licence types already saved", self.basedir, )
        else:
            self.logger.info("[%s] Saving licence types", self.basedir, )
            self.save_rights_data(self.openn_xml_path())
            self.write_status(self.SPREADSHEET_LICENCE_TYPES_SAVED)

        if self.get_status() > self.REPOSITORY_PREP_FILE_LIST_WRITTEN:
            self.logger.warning("[%s] File list already written", self.basedir, )
        else:
            self.logger.info("[%s] Writing file list", self.basedir, )
            file_list = self.build_file_list(self.openn_xml_path())
            self.add_file_list(file_list)
            self.write_status(self.REPOSITORY_PREP_FILE_LIST_WRITTEN)

        if self.get_status() > self.REPOSITORY_PREP_PARTIAL_TEI_WRITTEN:
            self.logger.warning("[%s] Partial TEI already written", self.basedir, )
        else:
            self.logger.info("[%s] Writing partial TEI", self.basedir, )
            partial_tei = self.build_partial_tei()
            # print partial_tei
            self.write_partial_tei(self.source_dir, partial_tei)
            self.validate_partial_tei()
            self.write_status(self.REPOSITORY_PREP_PARTIAL_TEI_WRITTEN)
            self.add_removal(self.openn_xml_path())
            self.archive_xlsx()
