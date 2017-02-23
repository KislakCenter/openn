from copy import deepcopy
from openn.openn_exception import OPennException

from openn.models import *

class RepositoryWrapper:
    def __init__(self, repository_config):
        self._config = deepcopy(repository_config)
        self._repository = None

    def repository(self):
        try:
            if self._repository is None:
                self._repository = Repository.objects.get(tag=self.tag())
        except Repository.DoesNotExist:
            raise OPennException("Could not find repository: %s" % (self.tag(),))

        return self._repository

    def config(self):
        return self._config

    def is_live(self):
        return self._config['live']

    def tag(self):
        return self._config['tag']

    def name(self):
        return self._config['name']

    def blurb(self):
        return self._config['blurb']

    def no_document(self):
        return self._config.get('no_document', False)

    def metadata_type(self):
        return self.repository().get_metadata_type_display()

    def long_id(self):
        return self.repository().long_id()

    def folder(self):
        oprepo = self.repository()
        if oprepo is not None:
            return oprepo.long_id()
        else:
            msg = "RepositoryWrapper with tag '%s' is not in db; has no folder"
            raise OPennException(msg % self.tag)

    def toc_file(self):
        return self.repository().toc_file()

    def csv_toc_file(self):
        return self.repository().csv_toc_file()

    def web_dir(self):
        return self.repository().web_dir()

    def html_dir(self):
        return self.repository().html_dir()

    def include_file(self):
        return self.config()['include_file']
