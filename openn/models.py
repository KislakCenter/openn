from django.db import models

class Document(models.Model):
    call_number   = models.CharField(max_length = 255, null = False, default = None)
    collection    = models.CharField(max_length = 30, null = False, default = None)
    base_dir      = models.CharField(max_length = 30, null = False, default = None)
    is_online     = models.BooleanField(default = False)
    tei_file_name = models.CharField(max_length = 40, null = True, default = None)
    created       = models.DateTimeField(auto_now_add = True)
    updated       = models.DateTimeField(auto_now = True)

    # Choosing collection, base_dir as the uniqueness columns
    # While the collection + call_number should be unique, the collection +
    # base_dir must be unique to prevent filesystem collisions on the host.
    class Meta:
        ordering        = ['collection', 'base_dir']
        unique_together = ('collection', 'base_dir')


    def __str__(self):
        return ("Document: id={id:d}, call_number={call_number}" +
                ", collection={collection}, base_dir={base_dir}" +
                ", is_online={is_online}, tei_file_name={tei_file_name}" +
                ", created={created}, updated={updated}").format(
                        id=self.id,
                        call_number=self.call_number,
                        collection=self.collection,
                        base_dir=self.base_dir,
                        is_online=self.is_online,
                        tei_file_name=self.tei_file_name,
                        created=self.created,
                        updated=self.updated)
