import os
import pytz

from datetime import datetime

from openn.prep.status import Status
from openn.prep.common_prep import CommonPrep
from openn.prep.prep_setup import PrepSetup
from openn.openn_exception import OPennException
from openn.models import PrepStatus
import subprocess
import logging

class OPennPrep:

    logger = logging.getLogger(__name__)

    def prep_dir(self, source_dir, prep_config, doc=None):
        try:
            prepstatus = None
            base_dir = os.path.basename(source_dir)
            status_txt = os.path.join(source_dir, 'status.txt')
            if not os.path.exists(status_txt):
                Status(source_dir).write_status(Status.PREP_BEGUN)

            setup = PrepSetup()
            repo_wrapper = prep_config.repository_wrapper()
            if doc is None:
                doc = setup.prep_document(repo_wrapper, base_dir)
            prepstatus = self._setup_prepstatus(doc)


            self.run_before(source_dir, prep_config)

            repo_prep_class = prep_config.get_prep_class()
            repo_prep = repo_prep_class(source_dir, doc, prep_config)
            repo_prep.prep_dir()

            if prep_config.process_directory():
                common_prep = CommonPrep(source_dir, doc, prep_config)
                common_prep.prep_dir()
            self._success_status(prepstatus)
            return doc
        except Exception as ex:
            if prepstatus is not None:
                self._failure_status(prepstatus, ex)
            raise

    def run_before(self, source_dir, prep_config):
        """Run any before scripts."""
        for script in prep_config.before_scripts():
            self.logger.info("Processing before script: %r", (script,))
            p = subprocess.Popen(script,
                                 stderr=subprocess.PIPE,
                                 stdout=subprocess.PIPE)
            out, err = p.communicate()
            print out
            print err
            if p.returncode != 0:
                # print err
                raise OPennException("Before script failed: %s", str(script))


    def update_tei(self, source_dir, document, prep_config, **kwargs):
        repo_prep_class = prep_config.get_prep_class()
        repo_prep = repo_prep_class(source_dir, document, prep_config)
        repo_prep.regen_partial_tei(document, **kwargs)
        repo_prep._cleanup()

        common_prep = CommonPrep(source_dir, document, prep_config)
        common_prep.update_document()
        common_prep.update_tei()
        common_prep._cleanup()

    def _setup_prepstatus(self, doc):
        # destroy the associate prep if it exists
        if hasattr(doc, 'prepstatus'):
            prepstatus = doc.prepstatus
            prepstatus.delete()
        prepstatus = PrepStatus(document=doc)
        prepstatus.save()
        return prepstatus

    def _success_status(self, prepstatus):
        prepstatus.finished  = datetime.now(pytz.utc)
        prepstatus.succeeded = True
        prepstatus.save()

    def _failure_status(self, prepstatus, ex):
        prepstatus.finished  = datetime.now(pytz.utc)
        prepstatus.succeeded = False
        prepstatus.error     = unicode(ex)
        prepstatus.save()
