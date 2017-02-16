# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        db.rename_table('openn_openncollection', 'openn_repository')


    def backwards(self, orm):
        db.rename_table('openn_repository','openn_openncollection')
