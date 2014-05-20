# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Document.colletion'
        db.add_column(u'openn_document', 'colletion',
                      self.gf('django.db.models.fields.CharField')(default='medrein', max_length=30),
                      keep_default=False)


        # Changing field 'Document.base_dir'
        db.alter_column(u'openn_document', 'base_dir', self.gf('django.db.models.fields.CharField')(default='x', max_length=30))

    def backwards(self, orm):
        # Deleting field 'Document.colletion'
        db.delete_column(u'openn_document', 'colletion')


        # Changing field 'Document.base_dir'
        db.alter_column(u'openn_document', 'base_dir', self.gf('django.db.models.fields.CharField')(max_length=30, null=True))

    models = {
        u'openn.document': {
            'Meta': {'object_name': 'Document'},
            'base_dir': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'call_number': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'colletion': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_online': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'tei_file_name': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['openn']