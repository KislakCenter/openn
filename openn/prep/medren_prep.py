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
from openn.openn_exception import OPennException
from openn.openn_functions import *
from openn.xml.openn_tei import OPennTEI

class MedrenPrep(RepositoryPrep):

    MEDREN_LICENCE_TYPES_SAVED = 65

    STATUS_NAMES = RepositoryPrep.build_status_names({
        65: 'MEDREN_LICENCE_TYPES_SAVED'
    })

    BLANK_RE = re.compile('blank', re.IGNORECASE)
    NEW_BIBID_RE = re.compile('^99\d+3503681$')
    DEFAULT_DOCUMENT_IMAGE_PATTERNS = [ 'front_?\d{4}\w*\.tif$', 'body_?\d{4}\w*\.tif$', 'back_?\d{4}\w*\.tif$' ]
    # 2017-11-13 DE: Accommodate odd file pattern:
    #
    #    cajs_rarms228_wk1_body_0003.tif
    #
    # typically, this file would be
    #
    #   cajs_rarms228_wk1_body0003.tif
    #
    # i.e., without '_' between `body` and `0003`.
    STRICT_IMAGE_PATTERN_RE = re.compile('^\w*_(front|body|back)_?\d{4}.tif$')

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

    @property
    def host(self):
        return self.pih_host

    @property
    def document_image_patterns(self):
        """The document_image_patterns property is an optional list of
        string patterns for selecting and ordering document image
        names; these strings must be valid regular expressions. If this
        value is not set, the default patterns will be used. They are:

            - ``[ 'front\d{4}\.tif$', 'body\d{4}\.tif$', 'back\d{4}\.tif$' ]``

        This list of patterns will be used by prep_file_list() to
        create a sorted file list of 'front', 'body', and 'back'
        images.

        """
        if getattr(self, '_document_image_patterns', None):
            return self._document_image_patterns
        else:
            return MedrenPrep.DEFAULT_DOCUMENT_IMAGE_PATTERNS

    @document_image_patterns.setter
    def document_image_patterns(self, pattern_list):
        self._document_image_patterns = pattern_list

    @document_image_patterns.deleter
    def document_image_patterns(self):
        del self._document_image_patterns

    @property
    def url_path(self):
        return self.pih_path

    # TODO: Add handling for holdingid.txt and holding_id

    def holdingid_filename(self):
        if not os.path.exists(self.source_dir):
            raise OPennException("Could not find source_dir: %s" % self.source_dir)
        holdingid_txt = os.path.join(self.source_dir, 'holdingid.txt')
        if not os.path.exists(holdingid_txt):
            return None
        return holdingid_txt

    def get_holdingid(self):
        holdingid_file = self.holdingid_filename()
        if holdingid_file is None:
            return None
        holdingid = open(holdingid_file).read().strip()
        return holdingid

    def bibid_filename(self):
        if not os.path.exists(self.source_dir):
            raise OPennException("Could not find source_dir: %s" % self.source_dir)
        bibid_txt = os.path.join(self.source_dir, 'bibid.txt')
        if not os.path.exists(bibid_txt):
            raise OPennException("Could not find bibid.txt: %s" % bibid_txt)
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
            raise OPennException("Penn in Hand XML lists no files: see %s" % pih_xml)
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
        r = tree.xpath("/page/result/xml/marc:record/marc:datafield[@tag='099']/marc:subfield[@code='a']", namespaces=ns)

        if len(r) < 1:
            raise OPennException('No call number found in PIH XML: %s' % pih_xml)

        call_no = r[0].text
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
        for tif in files.get('document'):
            base         = os.path.splitext(os.path.basename(tif['filename']))[0]
            # //xml[@name = 'pages']/page[@image = 'mscodex1223_wk1_back0001']
            query        = "//xml[@name = 'pages']/page[@image = '%s']" % base
            el           = xml.xpath(query)
            label        = el[0].get('visiblepage') if len(el) > 0 else None
            tif['label'] = self.prep_label(label)
        return files

    def include_file(self, filename, pttrn, expected_files):
        if re.search(pttrn, filename):
            base = os.path.basename(filename)
            return (base in expected_files) or self.STRICT_IMAGE_PATTERN_RE.match(base)

    def prep_file_list(self, expected):
        """" Create a list of TIFF file in the directroy. Split the list into
        'document' and 'extra' files. The 'document' files list
        comprises a all those that match the document_image_patterns.
        This list is sorted within each grouping specified by the
        patterns. The `extra` files list consists of all TIFF's that
        do not match the document image patterns. This list is not
        sorted.

        """
        files = glob.glob(os.path.join(self.data_dir, '*.tif'))
        files = [ self.source_dir_re.sub('', x) for x in files ]
        sorted_files = []
        # find all the files that match the pattern for document images
        for sec_pttrn in self.document_image_patterns:
            # temp_list     = filter(lambda x: re.search(sec_pttrn, x), files)
            sec_files     = filter(lambda x: self.include_file(x, sec_pttrn, expected), files)
            sec_files     = sorted(sec_files)
            sec_infos     = [ { 'filename': x, 'image_type': 'document' } for x in sec_files ]
            sorted_files += sec_infos
            # any file we've add selected; remove from the master file list
            for fileinfo in sec_infos: files.remove(fileinfo['filename'])

        # all the remaining files are extra
        files = [ { 'filename': x, 'image_type': 'extra', 'label': 'None' } for x in files ]
        return { 'document': sorted_files, 'extra': files }

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

    def regen_partial_tei(self, doc, **kwargs):
        xsl_command = ['op-gen-tei']
        tei = OPennTEI(doc.tei_xml)
        bibid = tei.bibid
        if bibid is None:
            raise OPennException("Whoah now. bibid is none. That ain't right.")
        if not self.NEW_BIBID_RE.match(bibid):
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

    def _do_prep_dir(self):
        if self.get_status() > self.REPOSITORY_PREP_MD_VALIDATED:
            self.logger.warning("[%s] Metadata alreaady validated", self.basedir)
        else:
            self.logger.info("[%s] Validating metadata", self.basedir)
            bibid = self.get_bibid()
            self.write_xml(bibid, self.pih_filename)
            call_no = self.check_valid_xml(self.pih_filename)
            self.write_status(self.REPOSITORY_PREP_MD_VALIDATED)

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
            self.fix_image_names()
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

        # files to cleanup
        self.add_removal(self.pih_filename)
        self.add_removal(self.bibid_filename())
        self.add_removal(self.holdingid_filename())
        self.add_removal(os.path.join(self.source_dir, 'sha1manifest.txt'))
