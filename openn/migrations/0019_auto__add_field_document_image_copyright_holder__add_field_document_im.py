# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Document.image_copyright_holder'
        db.add_column(u'openn_document', 'image_copyright_holder',
                      self.gf('django.db.models.fields.CharField')(default=None, max_length=255, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Document.image_copyright_year'
        db.add_column(u'openn_document', 'image_copyright_year',
                      self.gf('django.db.models.fields.IntegerField')(default=None, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Document.image_rights_more_info'
        db.add_column(u'openn_document', 'image_rights_more_info',
                      self.gf('django.db.models.fields.TextField')(default=None, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Document.metadata_copyright_holder'
        db.add_column(u'openn_document', 'metadata_copyright_holder',
                      self.gf('django.db.models.fields.CharField')(default=None, max_length=255, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Document.metadata_copyright_year'
        db.add_column(u'openn_document', 'metadata_copyright_year',
                      self.gf('django.db.models.fields.IntegerField')(default=None, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Document.metadata_rights_more_info'
        db.add_column(u'openn_document', 'metadata_rights_more_info',
                      self.gf('django.db.models.fields.TextField')(default=None, null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Document.image_copyright_holder'
        db.delete_column(u'openn_document', 'image_copyright_holder')

        # Deleting field 'Document.image_copyright_year'
        db.delete_column(u'openn_document', 'image_copyright_year')

        # Deleting field 'Document.image_rights_more_info'
        db.delete_column(u'openn_document', 'image_rights_more_info')

        # Deleting field 'Document.metadata_copyright_holder'
        db.delete_column(u'openn_document', 'metadata_copyright_holder')

        # Deleting field 'Document.metadata_copyright_year'
        db.delete_column(u'openn_document', 'metadata_copyright_year')

        # Deleting field 'Document.metadata_rights_more_info'
        db.delete_column(u'openn_document', 'metadata_rights_more_info')


    models = {
        u'openn.derivative': {
            'Meta': {'ordering': "['deriv_type']", 'object_name': 'Derivative'},
            'bytes': ('django.db.models.fields.IntegerField', [], {}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'deriv_type': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '20'}),
            'height': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': u"orm['openn.Image']"}),
            'path': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '255'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'width': ('django.db.models.fields.IntegerField', [], {})
        },
        u'openn.document': {
            'Meta': {'ordering': "['collection', 'base_dir', 'call_number']", 'unique_together': "(('collection', 'base_dir'),)", 'object_name': 'Document'},
            'base_dir': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '30'}),
            'call_number': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'collection': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '30'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image_copyright_holder': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'image_copyright_year': ('django.db.models.fields.IntegerField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'image_licence': ('django.db.models.fields.CharField', [], {'default': "'PD'", 'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'image_rights_more_info': ('django.db.models.fields.TextField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'is_online': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'metadata_copyright_holder': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'metadata_copyright_year': ('django.db.models.fields.IntegerField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'metadata_licence': ('django.db.models.fields.CharField', [], {'default': "'CC-BY'", 'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'metadata_rights_more_info': ('django.db.models.fields.TextField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'tei_xml': ('django.db.models.fields.TextField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.TextField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'openn.image': {
            'Meta': {'ordering': "('order',)", 'object_name': 'Image'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'document': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': u"orm['openn.Document']"}),
            'filename': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image_type': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'label': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '255'}),
            'order': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'openn.prepstatus': {
            'Meta': {'object_name': 'PrepStatus'},
            'document': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['openn.Document']", 'unique': 'True', 'primary_key': 'True'}),
            'error': ('django.db.models.fields.TextField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'finished': ('django.db.models.fields.DateTimeField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'started': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'succeeded': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'openn.version': {
            'Meta': {'ordering': "['document', 'major_version', 'minor_version', 'patch_version']", 'unique_together': "(['document', 'major_version', 'minor_version', 'patch_version'],)", 'object_name': 'Version'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'default': 'None'}),
            'document': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': u"orm['openn.Document']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'major_version': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'minor_version': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'order': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'patch_version': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['openn']