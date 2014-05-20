# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Document.base_dir'
        db.add_column(u'openn_document', 'base_dir',
                      self.gf('django.db.models.fields.CharField')(max_length=30, null=True),
                      keep_default=False)

        # Adding field 'Document.tei_file_name'
        db.add_column(u'openn_document', 'tei_file_name',
                      self.gf('django.db.models.fields.CharField')(max_length=40, null=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Document.base_dir'
        db.delete_column(u'openn_document', 'base_dir')

        # Deleting field 'Document.tei_file_name'
        db.delete_column(u'openn_document', 'tei_file_name')


    models = {
        u'openn.document': {
            'Meta': {'object_name': 'Document'},
            'base_dir': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True'}),
            'call_number': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_online': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'tei_file_name': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['openn']