import os
import httplib
import re
import urllib2
from lxml import etree
from openn.prep.collection_prep import CollectionPrep
from openn.openn_exception import OPennException
from openn.openn_functions import *

class MedrenPrep(CollectionPrep):

    def __init__(self, source_dir, host=None, path=None):
        """
        Create a new MedrenPrep for the given source_dir with metadata to be found
        on host at path. NB: path is a formattable string like:

             /dla/medren/pageturn.xml?id=MEDREN_{0}
            
        """
        self.source_dir = source_dir
        self.host       = host
        self.path       = path

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
        missing = []
        for file in expected:
            path = os.path.join(self.source_dir, file)
            if not os.path.exists(path):
                missing.append(file)
        if len(missing) > 0:
            smiss = ', '.join(missing)
            raise OPennException("Expected images are missing from %s: %s" % (self.source_dir, smiss))

    def check_valid_xml(self, pih_xml):
        f = open(pih_xml)
        tree = etree.parse(f)
        r = tree.xpath("/page/response/result/doc/arr[@name='call_number_field']/str")

        if len(r) < 1:
            raise OPennException('No call number found in PIH XML: %s' % pih_xml)

        call_no = r[0].text
        return call_no

    def full_url(self, bibid):
        return 'http://{0}{1}'.format(self.host, self.path.format(bibid))

    def check_url(self, bibid):
        conn = httplib.HTTPConnection(self.host)
        conn.request("HEAD", self.path.format(bibid))
        res = conn.getresponse()
        return res.status

    def get_xml(self, bibid):
        url = self.full_url(bibid)
        status = self.check_url(bibid)
        if status != 200:
            raise OPennException('Got status %d calling: %s' % (status, url))
        return urllib2.urlopen(url).read()
            
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
