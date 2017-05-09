# -*- coding: utf-8 -*-

from openn.csv.openn_csv import OPennCSV
from openn.models import *
import openn.openn_functions as opfunc
from unidecode import unidecode
import os
import re
import logging

class CuratedCollectionContentsCSV(OPennCSV):
    """Generate the table of contents CSV for an Repository

    The file `/Data/bibliophilly_contents.csv` looks like the following:

        curated_collection,   document_id,  path,             repository_id, metadata_type,  title,                  added
        biblio_philly,        1435,         0002/mscodex117,  0002,          TEI,            Alchemical miscellany,  2016-11-29 10:55:00
        biblio_philly,        288,          0001/ljs447,      0001,          TEI,            Masālik al-abṣār...,    2016-12-02 15:10:00
    """

    logger = logging.getLogger(__name__)

    HEADER      = 'curated_collection,document_id,path,repository_id,metadata_type,title,added'.split(',')
    REL_PATH_RE = re.compile('^/?Data/')


    def __init__(self, curated_tag, **kwargs):
        """
        Create a new CuratedCollectionContentsCSV object. Arguments:

        :outdir:        the output directory; for example ``/path/to/Data``

        :curated_tag:   tag for the curated collection

        """
        self.curated_collection    = CuratedCollection.objects.get(tag=unicode(curated_tag))
        outfile                    = os.path.join('Data', self.curated_collection.csv_toc_file())
        kwargs.update({'outfile': outfile})
        kwargs.update({'page_object': self.curated_collection})
        super(CuratedCollectionContentsCSV, self).__init__(**kwargs)

    def is_makeable(self):
        # if not live, we don't make the TOC
        if not self.curated_collection.live:
            self.logger.info("TOC not makeable; curated collection not set to 'live'"
                             " (curated collection: %s)", self.curated_collection.tag())
            return False

        if self.curated_collection.documents.count() == 0:
            self.logger.info("CSV TOC not makeable; curated collection has no"
                             " documents: %s", self.curated_collection.tag,)
            return False

        doc_count = self.curated_collection.documents.filter(is_online=True).count()
        if doc_count == 0:
            self.logger.info("CSV TOC not makeable; curated collection has"
                             " no documents online: %s", self.curated_collection.tag,)
            return False

        return True

    def is_needed(self, strict=True):
        # not needed if not makeable
        if not self.is_makeable() and strict is True:
            return False

        # needed if it doesn't exist
        if not os.path.exists(self.outfile_path()):
            return True

        # see if it's out-of-date
        latest_doc = self.curated_collection.curatedmembership_set.filter(
            document__is_online=True).latest('updated')
        current_file_date = opfunc.mtime_to_datetime(self.outfile_path())
        if current_file_date > latest_doc.updated:
            self.logger.debug("current_file_date: %s; latest_doc updated: %s", current_file_date,
                              latest_doc.updated)
            logging.info("CSV TOC up-to-date; skipping %s", self.curated_collection.tag)
            return False

        return True

    def write_file(self):
        """
            The file `/Data/bibliophilly_contents.csv` looks like the following:

                curated_collection,   document_id,  path,             repository_id, metadata_type,  title,                  added
                biblio_philly,        1435,         0002/mscodex117,  0002,          TEI,            Alchemical miscellany,  2016-11-29 10:55:00
                biblio_philly,        288,          0001/ljs447,      0001,          TEI,            Masālik al-abṣār...,    2016-12-02 15:10:00
        """
        try:
            self.writerow(CuratedCollectionContentsCSV.HEADER)
            memberships = self.curated_collection.curatedmembership_set.all()
            for membership in opfunc.queryset_iterator(memberships,chunksize=500):
                if membership.document.is_online:
                    doc = membership.document
                    rel_path = CuratedCollectionContentsCSV.REL_PATH_RE.sub('', doc.package_dir)
                    # Note that we use unidecode on the title to strip off
                    # diacritics and special characters. This is to make CSVs
                    # more broadly useable.
                row = [
                    self.curated_collection.tag,
                    str(doc.id),
                    rel_path,
                    doc.repository_id_long,
                    doc.metadata_type,
                    unidecode(doc.title),
                    opfunc.safe_isoformat(membership.created),
                    ]
                self.writerow(row)
        finally:
            self.close()
