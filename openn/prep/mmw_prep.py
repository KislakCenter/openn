# -*- coding: utf-8 -*-
import os
import json
import httplib
import re
import urllib2
import subprocess
import glob
import shutil
import logging
import sys
import codecs
import pytz
from lxml import etree
from datetime import datetime
from openn.prep.repository_prep import RepositoryPrep
from openn.prep.op_workbook import OPWorkbook
from openn.prep.spreadsheet_xml import SpreadsheetXML
from openn.openn_exception import OPennException
from openn.openn_functions import *
from openn.xml.openn_tei import OPennTEI

class MMWPrep(RepositoryPrep):

    SPREADSHEET_OPEN_XML_WRITTEN    = 60
    MEDREN_LICENCE_TYPES_SAVED = 65

    STATUS_NAMES = RepositoryPrep.build_status_names({
        60: 'SPREADSHEET_OPEN_XML_WRITTEN',
        65: 'MEDREN_LICENCE_TYPES_SAVED'
    })

    BLANK_RE = re.compile('blank', re.IGNORECASE)
    NEW_BIBID_RE = re.compile('^99\d+3681$')

    logger = logging.getLogger(__name__)

    def __init__(self, source_dir, document, prep_config):
        """Create a new MedrenPrep for the given 'source_dir' and document,
        and PrepConfig 'prep_config'.  'prep_config.prep_class_params()'
        must include:

            'pih_host'  the XML source URL host

            'pih_path'  a formattable string for the URL path for the
                        metadata; e.g.,
                        /dla/medren/pageturn.xml?id=MEDREN_{0}

            'xsl'       absolute path to the XSL to transform the XML to TEI

        """
        # TODO: break if SAXON_JAR not set; see bin/op-gen-tei
        RepositoryPrep.__init__(self,source_dir,document, prep_config)
        self.source_dir_re = re.compile('^%s/*' % source_dir)
        self.data_dir      = os.path.join(self.source_dir, 'data')
        self.pih_host      = prep_config.prep_class_parameter('pih_host')
        self.pih_path      = prep_config.prep_class_parameter('pih_path')
        self.xsl           = prep_config.prep_class_parameter('xsl')
        self._workbook     = None
        self._xsl          = prep_config.prep_class_parameter('xsl')
        config_json        = prep_config.prep_class_parameter('config_json')
        self._config       = json.load(open(config_json))

    @property
    def host(self):
        return self.pih_host

    @property
    def url_path(self):
        return self.pih_path

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

    def holdingid_filename(self):
        if not os.path.exists(self.source_dir):
            raise OPennException("Could not find source_dir: %s" % self.source_dir)
        holdingid_txt = os.path.join(self.source_dir, 'holdingid.txt')
        if not os.path.exists(holdingid_txt):
            return None
        return holdingid_txt

    def get_holdingid(self):
        try:
            self.holding_id
        except AttributeError:
            holdingid_file = self.holdingid_filename()
            if holdingid_file is None:
                self.holding_id = None
            else:
                self.holding_id = open(holdingid_file).read().strip()

        return self.holding_id

    def bibid_filename(self):
        if not os.path.exists(self.source_dir):
            raise OPennException("Could not find source_dir: %s" % self.source_dir)
        bibid_txt = os.path.join(self.source_dir, 'bibid.txt')
        if not os.path.exists(bibid_txt):
            return None
        return bibid_txt

    def get_bibid(self):
        bibid = open(self.bibid_filename()).read().strip()
        if not re.match('\d+$', bibid):
            raise OPennException("Bad BibID; expected only digits; found: '%s'" % bibid)
        if len(bibid) > 7:
            return bibid
        else:
            return '99%s3503681' % (str(bibid),)

    @property
    def pih_filename(self):
        return os.path.join(self.source_dir, 'descriptive.xml')

    def xml_file_names(self, openn_xml_path):
        names = []
        with open(openn_xml_path) as f:
            tree = etree.parse(f)
            names = tree.xpath('//file_name')
        return [ unicode(x.text, 'utf8') for x in names ]

    def check_file_names(self, expected):
        # print sys_file_names(source_dir)
        if len(expected) < 1:
            raise OPennException("Penn in Hand XML lists no files: see %s" % self.pih_filename)
        missing = []
        for file in expected:
            path = os.path.join(self.source_dir, file)
            if not os.path.exists(path):
                missing.append(file)
        if len(missing) > 0:
            smiss = ', '.join(missing)
            raise OPennException("Expected images are missing from %s: %s" % (self.source_dir, smiss))

    def check_valid_xml(self, pih_xml):
        tree = etree.parse(open(pih_xml))
        ns = { 'marc': 'http://www.loc.gov/MARC21/slim' }
        # TODO handle the holding ID
        if self.get_holdingid() is None:
            xpath = "//marc:holding/marc:call_number/text()"
            call_numbers = tree.xpath(xpath, namespaces=ns)
            if len(call_numbers) < 1:
                # no holdings; assume this is not Penn MARC
                xpath = "//marc:record/marc:datafield[@tag='500']/marc:subfield[@code='a' and starts-with(text(), 'Shelfmark:')]"
                call_numbers = tree.xpath(xpath, namespaces=ns)
                if len(call_numbers) < 1:
                    raise OPennException('No call number found in in MARC XML', pih_xml)
                call_no = call_numbers[0]
            elif len(call_numbers) > 1:
                raise OPennException('Please provide holding ID; more than one'
                        ' call number found in PIH XML: (%s)' % pih_xml)
            else:
                call_no = call_numbers[0]
        else:
            holdingid = self.get_holdingid()
            xpath = "//marc:holding_id[text() = '%s']/parent::marc:holding/marc:call_number/text()" % holdingid
            call_numbers = tree.xpath(xpath, namespaces=ns)
            if len(call_numbers) != 1:
                raise OPennException('Expected 1 call number for holding ID'
                        ' %s; found %d in PIH XML %s' % (self.get_holdingid(),
                            len(call_numbers), pih_xml))
            else:
                call_no = call_numbers[0]

        return call_no

    def full_url(self, bibid):
        return 'http://{0}{1}'.format(self.host, self.url_path.format(bibid))

    def check_url(self, bibid):
        conn = httplib.HTTPConnection(self.host)
        url = self.url_path.format(bibid)
        self.logger.info("===== Requesting: %s" % (url,))
        conn.request("HEAD", url)
        # conn.request("HEAD", self.url_path.format(bibid))
        res = conn.getresponse()
        return res.status

    def get_xml(self, bibid):
        url = self.full_url(bibid)
        status = self.check_url(bibid)
        if status not in (200,303):
            raise OPennException('Got status %d calling: %s' % (status, url))
        return urllib2.urlopen(url).read()

    def add_file_list(self,file_list):
        # file_list = self.get_file_list(pih_xml)
        outfile = os.path.join(self.source_dir, 'file_list.json')
        f = open(outfile, 'w')
        f.write(json.dumps(file_list))
        f.close()

    def prep_label(self,label):
        if label is None:
            return 'Unlabeled'
        if MedrenPrep.BLANK_RE.search(label):
            return re.sub(';.*$', '', label)
        else:
            return label

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

    def include_file(self, filename, pttrn, expected_files):
        if re.search(pttrn, filename):
            base = os.path.basename(filename)
            return (base in expected_files) or self.STRICT_IMAGE_PATTERN_RE.match(base)

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

    def write_xml(self,bibid,outfile):
        if os.path.exists(outfile):
            backup = '{0}-{1}'.format(outfile, tstamp())
            warning(__name__, 'Backing up existing XML file {0} to {1}'.format(outfile, backup))
            os.rename(outfile, backup)
        f = open(outfile, 'w+')
        f.write(self.get_xml(bibid))
        f.close()
        return outfile

    def gen_partial_tei(self):
        xsl_command = ['op-gen-tei']

        holdingid = self.get_holdingid()
        if holdingid is not None:
            xsl_command.append("-p HOLDING_ID=%s" % (str(holdingid),))
        xsl_command.append(self.pih_filename)
        xsl_command.append(self.xsl)
        p = subprocess.Popen(xsl_command, stderr=subprocess.PIPE,
                stdout=subprocess.PIPE)
        out, err = p.communicate()
        if p.returncode != 0:
            raise OPennException("TEI Generation failed: %s" % err)

        return out

    def is_new_bibid(self, bibid):
        return self.NEW_BIBID_RE.match(bibid)

    def regen_partial_tei(self, doc, **kwargs):
        xsl_command = ['op-gen-tei']
        tei = OPennTEI(doc.tei_xml)
        bibid = tei.bibid
        if bibid is None:
            raise OPennException("Whoah now. bibid is none. That ain't right.")
        if not is_new_bibid(bibid):
            bibid = '99%s3503681' % (str(bibid),)
        self.write_xml(bibid,self.pih_filename)
        for key in kwargs:
            key_value = '%s="%s"' % (key, kwargs[key])
            xsl_command.append(key_value)
        xsl_command.append(self.pih_filename)
        xsl_command.append(self.xsl)

        p = subprocess.Popen(xsl_command, stderr=subprocess.PIPE,
            stdout=subprocess.PIPE)
        out, err = p.communicate()
        if p.returncode != 0:
            raise OPennException("TEI Generation failed: %s" % err)

        self.write_partial_tei(self.source_dir, out)
        self.add_removal(self.pih_filename)

    def get_marc_xml(self):
        if os.path.exists(os.path.join(self.source_dir, 'bibid.txt')):
            bibid = self.get_bibid()
            self.write_xml(bibid, self.pih_filename)
        elif os.path.exists(os.path.join(self.source_dir, 'descriptive.xml')):
            pass

        # now read the structural metadata

    def _do_prep_dir(self):
        if self.get_status() > self.REPOSITORY_PREP_MD_VALIDATED:
            self.logger.warning("[%s] Metadata alreaady validated", self.basedir)
        else:
            self.logger.info("[%s] Validating metadata", self.basedir)
            self.get_marc_xml()
            self.check_valid_xml(self.pih_filename)
            self.write_status(self.REPOSITORY_PREP_MD_VALIDATED)

        if self.get_status() > self.REPOSITORY_PREP_FILES_VALIDATED:
            self.logger.warning("[%s] Files alreaady validated", self.basedir)
        else:
            self.logger.info("[%s] Validating files", self.basedir)
            self.validate_file_names()
            self.write_status(self.REPOSITORY_PREP_FILES_VALIDATED)

        if self.get_status() > self.REPOSITORY_PREP_FILES_STAGED:
            self.logger.warning("[%s] Files already staged", self.basedir)
        else:
            self.logger.info("[%s] Staging files", self.basedir)
            self.stage_images()
            self.write_status(self.REPOSITORY_PREP_FILES_STAGED)

        if self.get_status() > self.SPREADSHEET_OPEN_XML_WRITTEN:
            self.logger.warning("[%s] OPenn XML already written", self.basedir, )
        else:
            self.logger.info("[%s] Writing OPenn XML", self.basedir, )
            self.write_openn_xml(self.openn_xml_path())
            self.write_status(self.SPREADSHEET_OPEN_XML_WRITTEN)

        if self.get_status() > self.MEDREN_LICENCE_TYPES_SAVED:
            self.logger.warning("[%s] Licensce types already saved", self.basedir)
        else:
            self.logger.info("[%s] Staging files", self.basedir)
            self.save_rights_data()
            self.write_status(self.MEDREN_LICENCE_TYPES_SAVED)

        if self.get_status() > self.REPOSITORY_PREP_FILE_LIST_WRITTEN:
            self.logger.warning("[%s] File list already written", self.basedir)
        else:
            self.logger.info("[%s] Writing file list", self.basedir)
            file_list = self.build_file_list(self.openn_xml_path())
            self.add_file_list(file_list)
            self.write_status(self.REPOSITORY_PREP_FILE_LIST_WRITTEN)

        if self.get_status() > self.REPOSITORY_PREP_PARTIAL_TEI_WRITTEN:
            self.logger.warning("[%s] Partial TEI already written", self.basedir)
        else:
            self.logger.info("[%s] Writing partial TEI", self.basedir)
            partial_tei_xml = self.gen_partial_tei()
            self.write_partial_tei(self.source_dir, partial_tei_xml)
            self.validate_partial_tei()
            self.write_status(self.REPOSITORY_PREP_PARTIAL_TEI_WRITTEN)

        # files to cleanup
        self.add_removal(self.pih_filename)
        self.add_removal(self.bibid_filename())
        self.add_removal(self.holdingid_filename())
        self.add_removal(os.path.join(self.source_dir, 'sha1manifest.txt'))
