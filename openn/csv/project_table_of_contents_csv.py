# -*- coding: utf-8 -*-

from openn.csv.openn_csv import OPennCSV
from openn.models import *
import openn.openn_functions as opfunc
from unidecode import unidecode
import os
import re
import logging
import glob


class ProjectTableOfContentsCSV(OPennCSV):
    """Generate the table of contents CSV for an OPennCollection

    The file `/Data/bibliophilly_contents.csv` looks like the following:

        curated_collection,   document_id,  path,             repository_id, metadata_type,  title,                  added
        biblio_philly,        1435,         0002/mscodex117,  0002,          TEI,            Alchemical miscellany,  2016-11-29 10:55:00
        biblio_philly,        288,          0001/ljs447,      0001,          TEI,            Masālik al-abṣār...,    2016-12-02 15:10:00
    """

    logger = logging.getLogger(__name__)

    HEADER      = 'curated_collection,document_id,path,repository_id,metadata_type,title,added'.split(',')
    REL_PATH_RE = re.compile('^/?Data/')


    def __init__(self, project_tag, **kwargs):
        """
        Create a new ProjectTableOfContentsCSV object. Arguments:

        :outdir:        the output directory; for example ``/path/to/Data``

        :collection:    the openn.collections.collection.Collection object
                        for the collection

        """
        self.project    = Project.objects.get(tag=unicode(project_tag))
        outfile         = os.path.join('Data', self.project.csv_toc_file())
        kwargs.update({ 'outfile': outfile })
        super(ProjectTableOfContentsCSV, self).__init__(**kwargs)

    def is_makeable(self):
        # if not live, we don't make the TOC
        if not self.project.live:
            self.logger.info("TOC not makeable; collection not set to 'live' (collection: %s)" % (
                self.collection.tag()))
            return False

        # Not makeable if no live documents are in the collection
        doc_count = self.project.documents.filter(is_online=True).count()
        if doc_count == 0:
            self.logger.info("CSV TOC not makeable; project has no documents online: %s" % (self.project.tag,))
            return False

        return True

    def is_needed(self):
        # not needed if not makeable
        if not self.is_makeable():
            return False

        # needed if it doesn't exist
        if not os.path.exists(self.outfile_path()):
            return True

        # see if it's out-of-date
        latest_doc = Project.documents.filter(is_online=True).latest('updated')
        current_file_date = os.path.getmtime(self.outfile_path())
        if current_file_date > latest_doc.updated:
            logging.info("CSV TOC up-to-date; skipping %s" % (self.project.tag,))
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
            self.writerow(ProjectTableOfContentsCSV.HEADER)
            memberships = self.project.projectmembership_set.all()
            for membership in opfunc.queryset_iterator(memberships,chunksize=500):
                if membership.document.is_online:
                    doc = membership.document
                    rel_path = ProjectTableOfContentsCSV.REL_PATH_RE.sub('', doc.package_dir)
                    # Note that we use unidecode on the title to strip off
                    # diacritics and special characters. This is to make CSVs
                    # more broadly useable.
                row = [
                    self.project.tag,
                    str(doc.id),
                    rel_path,
                    doc.collection_id_long,
                    doc.metadata_type,
                    unidecode(doc.title),
                    str(membership.created),
                    ]
                self.writerow(row)
        finally:
            self.close()
