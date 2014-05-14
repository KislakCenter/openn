from django.db import models

class Document(models.Model):
    call_number = models.CharField(max_length=255)
    is_online = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
