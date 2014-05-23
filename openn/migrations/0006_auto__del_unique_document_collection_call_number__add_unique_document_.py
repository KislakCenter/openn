# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Removing unique constraint on 'Document', fields ['collection', 'call_number']
        db.delete_unique(u'openn_document', ['collection', 'call_number'])

        # Adding unique constraint on 'Document', fields ['collection', 'base_dir']
        db.create_unique(u'openn_document', ['collection', 'base_dir'])


    def backwards(self, orm):
        # Removing unique constraint on 'Document', fields ['collection', 'base_dir']
        db.delete_unique(u'openn_document', ['collection', 'base_dir'])

        # Adding unique constraint on 'Document', fields ['collection', 'call_number']
        db.create_unique(u'openn_document', ['collection', 'call_number'])


    models = {
        u'openn.document': {
            'Meta': {'ordering': "['collection', 'base_dir']", 'unique_together': "(('collection', 'base_dir'),)", 'object_name': 'Document'},
            'base_dir': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'call_number': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'collection': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_online': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'tei_file_name': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['openn']