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
from lxml import etree
from openn.prep.collection_prep import CollectionPrep
from openn.openn_exception import OPennException
from openn.openn_functions import *
from openn.xml.openn_tei import OPennTEI

class MedrenPrep(CollectionPrep):

    BLANK_RE = re.compile('blank', re.IGNORECASE)
    DEFAULT_DOCUMENT_IMAGE_PATTERNS = [ 'front\d{4}\.tif$', 'body\d{4}\.tif$', 'back\d{4}\.tif$' ]

    logger = logging.getLogger(__name__)

    def __init__(self, source_dir, collection, document):
        """
        Create a new MedrenPrep for the given source_dir with config dictionary `config`.
        Config should have:

            host  the XML source URL host

            path  a formattable string for the URL path for the metadata; e.g.,
                    /dla/medren/pageturn.xml?id=MEDREN_{0}

            xsl   absolute path to the XSL to transform the XML to TEI

        """
        # TODO: break if SAXON_JAR not set; see bin/op-gen-tei
        CollectionPrep.__init__(self,source_dir,collection, document)
        self.source_dir_re = re.compile('^%s/*' % source_dir)

    @property
    def host(self):
        return self.coll_config['host']

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
        return self.coll_config['path']

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
        return bibid

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

    def check_file_names(self, pih_xml):
        # print sys_file_names(source_dir)
        expected = self.xml_file_names(pih_xml)
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
        r = tree.xpath("/page/response/result/doc/arr[@name='call_number_field']/str")

        if len(r) < 1:
            raise OPennException('No call number found in PIH XML: %s' % pih_xml)

        call_no = r[0].text
        return call_no

    def full_url(self, bibid):
        return 'http://{0}{1}'.format(self.host, self.url_path.format(bibid))

    def check_url(self, bibid):
        conn = httplib.HTTPConnection(self.host)
        conn.request("HEAD", self.url_path.format(bibid))
        res = conn.getresponse()
        return res.status

    def get_xml(self, bibid):
        url = self.full_url(bibid)
        status = self.check_url(bibid)
        if status != 200:
            raise OPennException('Got status %d calling: %s' % (status, url))
        return urllib2.urlopen(url).read()

    def add_file_list(self,pih_xml):
        file_list = self.get_file_list(pih_xml)
        outfile = os.path.join(self.source_dir, 'file_list.json')
        f = open(outfile, 'w')
        f.write(json.dumps(file_list))
        f.close()

    def fix_tiff_names(self):
        space_re = re.compile('\s+')
        tiffs = glob.glob(os.path.join(self.source_dir, '*.tif'))
        for tiff in tiffs:
            basename = os.path.basename(tiff)
            if space_re.search(basename):
                new_name = os.path.join(self.source_dir,
                                        space_re.sub('_', basename))
                shutil.move(tiff, new_name)


    def stage_tiffs(self):
        """Move the TIFF files into the data directory"""
        self.data_dir = os.path.join(self.source_dir, 'data')
        if not os.path.exists(self.data_dir):
            os.mkdir(self.data_dir)
        tiffs = glob.glob(os.path.join(self.source_dir, '*.tif'))
        for x in tiffs:
           shutil.move(x, self.data_dir)

    def prep_label(self,label):
        if label is None:
            return 'Unlabeled'
        if MedrenPrep.BLANK_RE.search(label):
            return re.sub(';.*$', '', label)
        else:
            return label

    def get_file_list(self,pih_xml):
        files = self.prep_file_list()
        xml = etree.parse(open(pih_xml))
        for tif in files.get('document'):
            base         = os.path.splitext(os.path.basename(tif['filename']))[0]
            # //xml[@name = 'pages']/page[@image = 'mscodex1223_wk1_back0001']
            query        = "//xml[@name = 'pages']/page[@image = '%s']" % base
            el           = xml.xpath(query)
            label        = el[0].get('visiblepage') if len(el) > 0 else None
            tif['label'] = self.prep_label(label)
        return files

    def prep_file_list(self):
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
        for section in self.document_image_patterns:
            sec_files     = sorted(filter(lambda x: re.search(section, x), files))
            sec_files     = [ { 'filename': x, 'image_type': 'document' } for x in sec_files ]
            # any file we've add selected; remove from the master file list
            for pair in sec_files:
                files.remove(pair['filename'])
            sorted_files += sec_files
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
        # xsl_command = os.path.join(os.path.dirname(__file__), 'op-gen-tei')
        bibid = self.get_bibid()
        xsl_command = 'op-gen-tei'
        p = subprocess.Popen([xsl_command, self.pih_filename, self.coll_config['xsl']],
                stderr=subprocess.PIPE,
                stdout=subprocess.PIPE)
        out, err = p.communicate()
        if p.returncode != 0:
            raise OPennException("TEI Generation failed: %s" % err)

        return out

    def regen_partial_tei(self, doc, **kwargs):
        xsl_command = 'op-gen-tei'
        tei = OPennTEI(doc.tei_xml)
        bibid = tei.bibid
        if bibid is None:
            raise Exception("Whoah now. bibid is none. That ain't right.")
        self.write_xml(bibid,self.pih_filename)
        p = subprocess.Popen([xsl_command, self.pih_filename, self.coll_config['xsl']],
                stderr=subprocess.PIPE,
                stdout=subprocess.PIPE)
        out, err = p.communicate()
        if p.returncode != 0:
            raise OPennException("TEI Generation failed: %s" % err)

        self.write_partial_tei(self.source_dir, out)
        self.add_removal(self.pih_filename)

    def _do_prep_dir(self):
        bibid = self.get_bibid()
        self.write_xml(bibid, self.pih_filename)
        call_no = self.check_valid_xml(self.pih_filename)
        self.check_file_names(self.pih_filename)
        self.fix_tiff_names()
        self.stage_tiffs()
        self.add_file_list(self.pih_filename)
        partial_tei_xml = self.gen_partial_tei()
        self.write_partial_tei(self.source_dir, partial_tei_xml)

        # files to cleanup
        self.add_removal(self.pih_filename)
        self.add_removal(self.bibid_filename())
        self.add_removal(os.path.join(self.source_dir, 'sha1manifest.txt'))
