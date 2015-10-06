import os
from datetime import datetime

from openn.prep.status import Status
from openn.prep.common_prep import CommonPrep
from openn.prep.prep_setup import PrepSetup
from openn.openn_exception import OPennException
from openn.models import PrepStatus

class OPennPrep:

    def prep_dir(self, source_dir, prep_config):
        try:
            base_dir = os.path.basename(source_dir)
            status_txt = os.path.join(source_dir, 'status.txt')
            if not os.path.exists(status_txt):
                Status(source_dir).write_status(Status.PREP_BEGUN)

            setup = PrepSetup()
            coll = prep_config.collection()
            doc = setup.prep_document(coll, base_dir)
            prepstatus = self._setup_prepstatus(doc)

            coll_prep_class = prep_config.get_prep_class()
            coll_prep = coll_prep_class(source_dir, doc, prep_config)
            coll_prep.prep_dir()

            common_prep = CommonPrep(source_dir, doc, prep_config)
            common_prep.prep_dir()
            self._success_status(prepstatus)
            return doc
        except Exception as ex:
            self._failure_status(prepstatus, ex)
            raise

    def update_tei(self, source_dir, document, prep_config):
        coll_prep_class = prep_config.get_prep_class()
        coll_prep = coll_prep_class(source_dir, document, prep_config)
        coll_prep.regen_partial_tei(document)
        coll_prep._cleanup()

        common_prep = CommonPrep(source_dir, document, prep_config)
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
        prepstatus.finished  = datetime.now()
        prepstatus.succeeded = True
        prepstatus.save()

    def _failure_status(self, prepstatus, ex):
        prepstatus.finished  = datetime.now()
        prepstatus.succeeded = False
        prepstatus.error     = str(ex)
        prepstatus.save()
