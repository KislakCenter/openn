# -*- coding: utf-8 -*-

from openn.csv.openn_csv import OPennCSV
from openn.models import *
import openn.openn_functions as opfunc
from unidecode import unidecode
import os
import re
import logging
import glob

class TableOfContentsCSV(OPennCSV):
    """Generate the table of contents CSV for an Repository

    The file `/Data/0002_contents.csv` looks like the following:

        document_id,  path,                   title,                              metadata_type,  created,              updated
        1435,         0002/mscodex901         "Il finto Policare, tragicomedia",  TEI             2015-10-15 13:02:00,  2015-10-15 08:22:00
        1710,         0002/mscoll764_item84,  Some title,                         TEI             2016-02-21 16:13:11,  2016-02-23 09:55:38
        1711,         0002/mscoll764_item85,  Some title,                         TEI             2016-02-21 16:13:30,  2016-02-23 09:55:38
        1712,         0002/mscoll764_item86,  Some title,                         TEI             2016-02-21 16:13:55,  2016-02-23 09:55:38
    """

    logger = logging.getLogger(__name__)

    HEADER      = 'document_id,path,title,metadata_type,created,updated'.split(',')
    REL_PATH_RE = re.compile('^/?Data/')


    def __init__(self, repository, **kwargs):
        """
        Create a new TableOfContentsCSV object. Arguments:

        :outdir:        the output directory; for example ``/path/to/Data``

        :repository:    the openn.repository.repository.Collection object
                        for the repository

        """
        self.repository = repository
        outfile         = os.path.join('Data', repository.csv_toc_file())
        kwargs.update({'outfile': outfile})
        kwargs.update({'page_object': self.repository})
        super(TableOfContentsCSV, self).__init__(**kwargs)


    def is_makeable(self):
        # if not live, we don't make the TOC
        if not self.repository.is_live():
            self.logger.info("TOC not makeable; repository not set to 'live' (repository: %s)" % (
                self.repository.tag()))
            return False

        # If this is a no-document repository, it is NOT makeable; we don't
        # have to look for an `html` dir or the files in it.
        #
        # NOTE: This is different from the regular TOC files; here, if there
        # are no documents, the CSV file will have no content.
        if self.repository.no_document():
            self.logger.info("CSV TOC not makeable; no document repository: %s" % (self.repository.tag(),))
            return False

        # Not makeable if no live documents are in the repository
        doc_count = Document.objects.filter(
            repository=self.repository.repository(),
            is_online=True
            ).count()
        if doc_count == 0:
            self.logger.info("CSV TOC not makeable; repository has no documents online: %s" % (self.repository.tag(),))
            return False

        # see if there are any HTML files for this repository
        # if there's no HTML dir there aren't any files
        html_dir = os.path.join(self.outdir, self.repository.html_dir())
        if not os.path.exists(html_dir):
            self.logger.info("CSV TOC not makeable; no HTML dir found: %s (repository: %s)" % (
                html_dir, self.repository.tag()))
            return False
        # OK, html dir is present; look for files
        html_files = glob.glob(os.path.join(html_dir, '*.html'))
        if len(html_files) == 0:
            self.logger.info("CSV TOC not makeable; no HTML files found in %s (repository %s)" % (
                html_dir, self.repository.tag()))
            return False

        return True

    def is_needed(self):
        # not needed if not makeable
        if not self.is_makeable():
            return False

        # needed if it doesn't exist
        if not os.path.exists(self.outfile_path()):
            self.logger.info("CSV is needed; file does not exist: %s", self.outfile_path())
            return True

        # see if it's out-of-date
        latest_doc = Document.objects.filter(
            repository=self.repository.repository(),
            is_online=True
            ).latest('updated')
        current_file_date = opfunc.mtime_to_datetime(self.outfile_path())

        if current_file_date > latest_doc.updated:
            logging.info("CSV TOC up-to-date; skipping %s", self.repository.tag())
            return False

        return True

    def write_file(self):
        try:
            self.writerow(TableOfContentsCSV.HEADER)
            docs = Document.objects.filter(
                repository=self.repository.repository(),
                is_online=True)
            for doc in opfunc.queryset_iterator(docs, chunksize=500):
                rel_path = TableOfContentsCSV.REL_PATH_RE.sub('', doc.package_dir)
                # Note that we use unidecode on the title to strip off
                # diacritics and special characters. This is to make CSVs
                # more broadly useable.
                row = [
                    str(doc.id),
                    rel_path,
                    unidecode(doc.title),
                    self.repository.metadata_type(),
                    opfunc.safe_isoformat(doc.created),
                    opfunc.safe_isoformat(doc.updated),
                    ]
                self.writerow(row)
        finally:
            self.close()
