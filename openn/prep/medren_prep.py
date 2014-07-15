import os
import json
import httplib
import re
import urllib2
import subprocess
import glob
import shutil
from lxml import etree
from openn.prep.collection_prep import CollectionPrep
from openn.openn_exception import OPennException
from openn.openn_functions import *

class MedrenPrep(CollectionPrep):

    BLANK_RE = re.compile('blank', re.IGNORECASE)

    def __init__(self, source_dir, collection):
        """
        Create a new MedrenPrep for the given source_dir with config dictionary `config`.
        Config should have:

            host  the XML source URL host

            path  a formattable string for the URL path for the metadata; e.g.,
                    /dla/medren/pageturn.xml?id=MEDREN_{0}

            xsl   absolute path to the XSL to transform the XML to TEI

        """
        CollectionPrep.__init__(self,collection)
        self.source_dir    = source_dir
        self.source_dir_re = re.compile('^%s/*' % source_dir)

    @property
    def host(self):
        return self.coll_config['host']

    @property
    def url_path(self):
        return self.coll_config['path']

    def write_tei(self, xml_path, xsl_path):
        outfile = os.path.join(self.source_dir, 'PARTIAL_TEI.xml')
        f = open(outfile, 'w')
        f.write(self.gen_tei(xml_path, xsl_path))
        f.close()
        return outfile

    def gen_tei(self, xml_path, xsl_path):
        # xsl_command = os.path.join(os.path.dirname(__file__), 'op-gen-tei')
        xsl_command = 'op-gen-tei'
        p = subprocess.Popen([xsl_command, xml_path, xsl_path],
                stderr=subprocess.PIPE,
                stdout=subprocess.PIPE)
        out, err = p.communicate()
        if p.returncode != 0:
            raise OPennException("TEI Generation failed: %s" % err)
        return out

    def get_bibid(self):
        if not os.path.exists(self.source_dir):
            raise OPennException("Could not find source_dir: %s" % self.source_dir)
        bibid_txt = os.path.join(self.source_dir, 'bibid.txt')
        if not os.path.exists(bibid_txt):
            raise OPennException("Could not find bibid.txt: %s" % bibid_txt)
        bibid = open(bibid_txt).read().strip()
        if not re.match('\d+$', bibid):
            raise OPennException("Bad BibID; expected only digits; found: '%s'" % bibid)
        return bibid

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
            return 'Blank'
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
        files = glob.glob(os.path.join(self.data_dir, '*.tif'))
        files = [ self.source_dir_re.sub('', x) for x in files ]
        sorted_files = []
        for section in ('front', 'body', 'back'):
            sec_files     = sorted(filter(lambda x: section  in x, files))
            sec_files     = [ { 'filename': x, 'image_type': 'document' } for x in sec_files ]
            for pair in sec_files:
                files.remove(pair['filename'])
            sorted_files += sec_files
        files = [ { 'filename': x, 'image_type': 'extra' } for x in files ]
        return { 'document': sorted_files, 'extra': files }

    def write_xml(self):
        bibid = self.get_bibid()
        outfile = os.path.join(self.source_dir, 'pih_{0}.xml'.format(bibid))
        if os.path.exists(outfile):
            backup = '{0}-{1}'.format(outfile, tstamp())
            warning(cmd(), 'Backing up existing XML file {0} to {1}'.format(outfile, backup))
            os.rename(outfile, backup)
        f = open(outfile, 'w+')
        f.write(self.get_xml(bibid))
        f.close()
        return outfile

    def prep_dir(self):
        pih_xml = self.write_xml()
        call_no = self.check_valid_xml(pih_xml)
        self.check_file_names(pih_xml)
        self.stage_tiffs()
        self.add_file_list(pih_xml)
        tei_xml = self.write_tei(pih_xml, self.coll_config['xsl'])
