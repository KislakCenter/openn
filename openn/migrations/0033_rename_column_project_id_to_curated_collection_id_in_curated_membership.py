# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        db.rename_column('openn_curatedmembership', 'project_id', 'curated_collection_id')

    def backwards(self, orm):
        db.rename_column('openn_curatedmembership', 'curated_collection_id', 'project_id')

    complete_apps = ['openn']