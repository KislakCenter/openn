from django.db import models

class Document(models.Model):
    call_number   = models.CharField(max_length = 255, null = False)
    collection    = models.CharField(max_length = 30, null = False)
    base_dir      = models.CharField(max_length = 30, null = False)
    is_online     = models.BooleanField(default = False)
    tei_file_name = models.CharField(max_length = 40, null = True)
    created       = models.DateTimeField(auto_now_add = True)
    updated       = models.DateTimeField(auto_now = True)

    class Meta:                                          
        ordering        = ['collection', 'call_number']
        unique_together = ('collection', 'call_number')

