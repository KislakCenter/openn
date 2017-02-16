# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        db.rename_column('openn_document', 'openn_collection_id', 'repository_id')

    def backwards(self, orm):
        db.rename_column('openn_document', 'repository_id', 'openn_collection_id')

