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
from openn.prep.marc_validator import MarcValidator

class MMWPrep(RepositoryPrep):

    SPREADSHEET_OPEN_XML_WRITTEN = 21
    MMW_PREP_PAGES_MERGED        = 30
    MEDREN_LICENCE_TYPES_SAVED   = 65
    MARC_XML_STAGED              = 87

    STATUS_NAMES = RepositoryPrep.build_status_names({
        21: 'SPREADSHEET_OPEN_XML_WRITTEN',
        30: 'MMW_PREP_PAGES_MERGED',
        65: 'MEDREN_LICENCE_TYPES_SAVED',
        87: 'MARC_XML_STAGED',
    })

    BLANK_RE = re.compile('blank', re.IGNORECASE)
    NEW_BIBID_RE = re.compile('^99\d+3681$')

    logger = logging.getLogger(__name__)

    def __init__(self, source_dir, document, prep_config):
        """Create a new MMWPrep for the given 'source_dir' and document,
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
        self.source_dir_re   = re.compile('^%s/*' % source_dir)
        self.data_dir        = os.path.join(self.source_dir, 'data')
        self.pih_host        = prep_config.prep_class_parameter('pih_host')
        self.pih_path        = prep_config.prep_class_parameter('pih_path')
        self.xsl             = prep_config.prep_class_parameter('xsl')
        self.merge_pages_xsl = prep_config.prep_class_parameter('merge_pages_xsl')
        self._workbook       = None
        self._xsl            = prep_config.prep_class_parameter('xsl')
        config_json          = prep_config.prep_class_parameter('config_json')
        self._config         = json.load(open(config_json))

    @property
    def host(self):
        return self.pih_host

    @property
    def url_path(self):
        return self.pih_path

    @property
    def xlsx_path(self):
        return os.path.join(self.source_dir, 'pages.xlsx')

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

    def check_file_names(self, expected):
        # print sys_file_names(source_dir)
        if len(expected) < 1:
            raise OPennException("Penn in Hand XML lists no files: see %s" % pih_xml)
        missing = []
        for file in expected:
            path = os.path.join(self.source_dir, file)
            if not os.path.exists(path):
                missing.append(file)
        if len(missing) > 0:
            smiss = ', '.join(missing)
            raise OPennException("Expected images are missing from %s: %s" % (self.source_dir, smiss))

    @property
    def openn_xml_path(self):
        return os.path.join(self.source_dir, 'pages.xml')

    def write_openn_xml(self,outfile):
        if os.path.exists(outfile):
            warning(__name__, 'Removing existing OPenn XML: %s' % (outfile))
            os.remove(outfile)
        with open(outfile, 'w+') as f:

            sp_xml = SpreadsheetXML(self.prep_config.context_var('licences'))
            xml = sp_xml.build_xml(self.workbook().data(), self._config['xml_config'])
            f.write(xml.encode('utf-8'))

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

        expected = [ os.path.join('data', x)
                     for x in self.xml_file_names(pih_xml) ]
        files    = self.prep_file_list(expected)
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

    @property
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
            holdingid_file = self.holdingid_filename
            if holdingid_file is None:
                self.holding_id = None
            else:
                self.holding_id = open(holdingid_file).read().strip()

        return self.holding_id

    @property
    def bibid_filename(self):
        if not os.path.exists(self.source_dir):
            raise OPennException("Could not find source_dir: %s" % self.source_dir)
        bibid_txt = os.path.join(self.source_dir, 'bibid.txt')
        if not os.path.exists(bibid_txt):
            return None
        return bibid_txt

    def get_bibid(self):
        bibid = open(self.bibid_filename).read().strip()
        if not re.match('\d+$', bibid):
            raise OPennException("Bad BibID; expected only digits; found: '%s'" % bibid)
        if len(bibid) > 7:
            return bibid
        else:
            return '99%s3503681' % (str(bibid),)

    @property
    def marc_xml(self):
        return os.path.join(self.source_dir, 'marc.xml')

    @property
    def pih_filename(self):
        return os.path.join(self.source_dir, 'pih.xml')

    def xml_file_names(self, pih_xml):
        # //xml[@name='pages']/page/@image
        f = open(pih_xml)
        tree = etree.parse(f)
        r = tree.xpath('//xml[@name="pages"]/page/@image')
        for i in range(len(r)):
            r[i] += '.tif'
        return r

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

    def check_valid_xml(self, marc_xml):
        xml_io = open(marc_xml)
        required_xpaths = self.prep_config.prep_class_parameter('required_xpaths')
        holdings_id = self.get_holdingid()
        marc_validator = MarcValidator(xml_io, required_xpaths, holdings_id)
        marc_validator.validate()
        if len(marc_validator.errors) > 0:
            # print marc_validator.errors
            self.logger.error(marc_xml)
            for err in marc_validator.errors:
                self.logger.error(err)
            raise OPennException("Errors found in MARC XML: %s\n" % ('\n'.join(marc_validator.errors),))

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
        if MMWPrep.BLANK_RE.search(label):
            return re.sub(';.*$', '', label)
        else:
            return label

    def include_file(self, filename, pttrn, expected_files):
        if re.search(pttrn, filename):
            base = os.path.basename(filename)
            return (base in expected_files) or self.STRICT_IMAGE_PATTERN_RE.match(base)

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
        # validate directory
        # Move files:
        #
        #  - pages.xlsx     required
        #  - marc.xml       required unless bibid.txt present
        #  - bibid.txt      ignored; BibID should be in existing TEI
        #  - holdingid.txt  optional; may be required for Penn MSS (with BibID in TEI)

        data_dir = kwargs.get('METADATA_DIR', None)
        if data_dir is None or data_dir.strip() == '':
            raise OPennException("Missing required METADATA_DIR")

        if not os.path.exists(data_dir):
            raise OPennException("Cannot find METADATA_DIR: '%s'" % (data_dir,))

        metadata_files = ('pages.xlsx', 'marc.xml', 'holdingid.txt')
        for file in metadata_files:
            full_path = os.path.abspath(os.path.join(data_dir, file))
            if os.path.exists(full_path):
                dest = os.path.abspath(os.path.join(self.source_dir, file))
                if full_path == dest:
                    pass
                elif os.path.exists(full_path):
                    shutil.copyfile(full_path, dest)

        tei = OPennTEI(doc.tei_xml)
        bibid = tei.bibid

        # make sure we have the marc.xml file
        if bibid is None:
            if os.path.exists(self.marc_xml):
                pass
            else:
                OPennException("Saved TEI lacks BibID; required MARC file missing: '%s'" % (self.marc_xml,))
        else:
            if not self.NEW_BIBID_RE.match(bibid):
                bibid = '99%s3503681' % (str(bibid),)
            self.write_xml(bibid, self.marc_xml)

        # create pages.xml from the page.xlsx
        self.write_openn_xml(self.openn_xml_path)
        # fake the pih.xml by merging pages.xml with marc.xml (from above)
        self.write_pih_xml()
        self.save_rights_data()
        partial_tei_xml = self.gen_partial_tei()
        self.write_partial_tei(self.source_dir, partial_tei_xml)
        self.validate_partial_tei()
        self.stage_marc_xml()

        self.add_removal(self.pih_filename)
        self.add_removal(self.bibid_filename)
        self.add_removal(self.holdingid_filename)
        self.add_removal(self.openn_xml_path)
        self.add_removal(self.xlsx_path)
        self.add_removal(os.path.join(self.source_dir, 'sha1manifest.txt'))

    def get_marc_xml(self):
        if os.path.exists(os.path.join(self.source_dir, 'bibid.txt')):
            bibid = self.get_bibid()
            self.write_xml(bibid, self.marc_xml)
        elif os.path.exists(os.path.join(self.source_dir, 'marc.xml')):
            pass

    def write_pih_xml(self):
        xsl_command = ['op-gen-tei']
        xsl_command.append("-p MARC_PATH=%s" % (os.path.abspath(self.marc_xml),))
        xsl_command.append(os.path.abspath(self.openn_xml_path))
        xsl_command.append(os.path.abspath(self.merge_pages_xsl))
        p = subprocess.Popen(xsl_command, stderr=subprocess.PIPE,
            stdout=subprocess.PIPE)
        out, err = p.communicate()
        if p.returncode != 0:
            raise OPennException("MARC/pages XML merge failed: %s" (err,))

        with open(self.pih_filename, 'w+') as f:
            f.write(out)

    def stage_marc_xml(self):
        if not os.path.exists(self.data_dir):
            os.mkdir(self.data_dir)
        shutil.move(self.marc_xml, self.data_dir)

    def _do_prep_dir(self):
        # create pages.xml from the page.xlsx
        if self.get_status() > self.SPREADSHEET_OPEN_XML_WRITTEN:
            self.logger.warning("[%s] OPenn XML already written", self.basedir, )
        else:
            self.logger.info("[%s] Writing OPenn XML", self.basedir, )
            self.write_openn_xml(self.openn_xml_path)
            self.write_status(self.SPREADSHEET_OPEN_XML_WRITTEN)

        # ensure we have marc.xml as a file from marmite
        if self.get_status() > self.REPOSITORY_PREP_MD_VALIDATED:
            self.logger.warning("[%s] Metadata alreaady validated", self.basedir)
        else:
            self.logger.info("[%s] Validating metadata", self.basedir)
            self.get_marc_xml()
            self.check_valid_xml(self.marc_xml)
            self.write_status(self.REPOSITORY_PREP_MD_VALIDATED)

        # fake the pih.xml by merging pages.xml with marc.xml
        if self.get_status() > self.MMW_PREP_PAGES_MERGED:
            self.logger.warning("[%s] Pages alreaady merged", self.basedir)
        else:
            self.logger.info("[%s] Merging pages XML", self.basedir)
            self.write_pih_xml()
            self.write_status(self.MMW_PREP_PAGES_MERGED)

        if self.get_status() > self.REPOSITORY_PREP_FILES_VALIDATED:
            self.logger.warning("[%s] Files alreaady validated", self.basedir)
        else:
            self.logger.info("[%s] Validating files", self.basedir)
            expected_files = self.xml_file_names(self.pih_filename)
            self.check_file_names(expected_files)
            self.write_status(self.REPOSITORY_PREP_FILES_VALIDATED)

        if self.get_status() > self.REPOSITORY_PREP_FILES_STAGED:
            self.logger.warning("[%s] Files already staged", self.basedir)
        else:
            self.logger.info("[%s] Staging files", self.basedir)
            self.stage_images()
            self.write_status(self.REPOSITORY_PREP_FILES_STAGED)

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
            file_list = self.build_file_list(self.pih_filename)
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

        if self.get_status() > self.MARC_XML_STAGED:
            self.logger.warning("[%s] marc.xml already staged", self.basedir)
        else:
            self.logger.info("[%s] Staging marc.xml", self.basedir)
            self.stage_marc_xml()
            self.write_status(self.MARC_XML_STAGED)

        # files to cleanup
        self.add_removal(self.marc_xml)
        self.add_removal(self.bibid_filename)
        self.add_removal(self.holdingid_filename)
        self.add_removal(self.pih_filename)
        self.add_removal(self.openn_xml_path)
        self.add_removal(self.xlsx_path)
        self.add_removal(os.path.join(self.source_dir, 'sha1manifest.txt'))
