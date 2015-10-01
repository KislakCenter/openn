from openn.prep.status import Status
from openn.openn_exception import OPennException

class OPennPrep:
    def __init__(self, prep_config, source_dir):
        self._prep_config = prep_config
        self._source_dir  = source_dir

    def prep_dir(self):
        base_dir = os.path.basename(self._source_dir)
        status_txt = os.path.join(source_dir, 'status.txt')
        if not os.path.exists(status_txt):
            Status(source_dir).write_status(Status.PREP_BEGUN)

        setup = PrepSetup()
        coll_config = self._prep_config.collection()
        doc = setup.prep_document(coll_config, base_dir)
        prepstatus = self._setup_prepstatus(doc)
        collection_prep =


    def _setup_prepstatus(self,doc):
        # destroy the associate prep if it exists
        if hasattr(doc, 'prepstatus'):
            prepstatus = doc.prepstatus
            prepstatus.delete()
        prepstatus = PrepStatus(document=doc)
        prepstatus.save()
        return prepstatus
