# -*- coding: utf-8 -*-

from openn.csv.openn_csv import OPennCSV
from openn.models import *

class CollectionsCSV(OPennCSV):
    """Generate CSV table of contents for all collections. Looks like this (without padding):

    repository_id,  collection_tag, collection_type,  metadata_type,  collection_name
    0001,           ljs,            repository,       TEI,            Lawrence J. Schoenberg Manuscripts
    0002,           pennmss,        repository,       TEI,            University of Pennsylvania Books & Manuscripts
    0003,           brynmawr,       repository,       TEI,            Bryn Mawr College Library Special Collections
    0004,           drexarc,        repository,       TEI,            Drexel University Archives and Special Collections
    N/A,            bibliophilly,   curated,          N/A,            Bibliotheca Philadelphiensis
    """
    HEADER = 'repository_id,collection_tag,collection_type,metadata_type,collection_name'.split(',')

    """docstring for CollectionsCSV"""
    def __init__(self, repo_configs, **kwargs):
        self.repo_configs = repo_configs
        outfile           = os.path.join('Data', 'collections.csv')
        kwargs.update({ 'outfile': outfile })
        super(CollectionsCSV, self).__init__(**kwargs)

    def write_file(self):
        try:
            self.writerow(CollectionsCSV.HEADER)
            for repo_wrapper in self.repo_configs.all_repositories():
                if repo_wrapper.is_live():
                    row = [
                        repo_wrapper.long_id(),
                        repo_wrapper.tag(),
                        'repository',
                        repo_wrapper.metadata_type(),
                        repo_wrapper.name(),
                        ]
                    self.writerow(row)

            for curated in CuratedCollection.objects.all():
                if curated.live:
                    row = [
                        'N/A',
                        curated.tag,
                        'curated',
                        'N/A',
                        curated.name,
                        ]
                    self.writerow(row)
        finally:
            # make sure we close the file
            self.close()

    def is_makeable(self):
        return True

    def is_needed(self):
        return self.is_makeable()
