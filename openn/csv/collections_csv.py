# -*- coding: utf-8 -*-

from openn.csv.openn_csv import OPennCSV
from openn.models import *

class CollectionsCSV(OPennCSV):
    """Generate CSV table of contents for all collections. Looks like this (without padding):

    collection_id,  collection_tag, collection_type,  metadata_type,  collection_name
    0001,           ljs,            repository,       OPENN-TEI,      Lawrence J. Schoenberg Manuscripts
    0002,           pennmss,        repository,       OPENN-TEI,      University of Pennsylvania Books & Manuscripts
    0003,           brynmawr,       repository,       OPENN-TEI,      Bryn Mawr College Library Special Collections
    0004,           drexarc,        repository,       OPENN-TEI,      Drexel University Archives and Special Collections
    N/A,            bibliophilly,   curated,          N/A,            Bibliotheca Philadelphiensis
    """
    HEADER = 'collection_id,collection_tag,collection_type,metadata_type,collection_name'.split(',')

    """docstring for CollectionsCSV"""
    def __init__(self, outdir, filename, coll_configs):
        self.coll_configs = coll_configs
        super(CollectionsCSV, self).__init__(outdir=outdir, filename=filename)

    def write_file(self):
        try:
            self.writerow(CollectionsCSV.HEADER)
            for coll_wrapper in self.coll_configs.all_collections():
                row = [
                    coll_wrapper.long_id(),
                    coll_wrapper.tag(),
                    'repository',
                    coll_wrapper.metadata_type(),
                    coll_wrapper.name(),
                    ]
                self.writerow(row)

            for project in Project.objects.all():
                row = [
                    'N/A',
                    project.tag,
                    'curated',
                    'N/A',
                    project.name,
                    ]
                self.writerow(row)
        finally:
            # make sure we close the file
            self.close()
