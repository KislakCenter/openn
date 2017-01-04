# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ProjectMembership'
        db.create_table(u'openn_projectmembership', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('document', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['openn.Document'])),
            ('project', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['openn.Project'])),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'openn', ['ProjectMembership'])

        # Adding unique constraint on 'ProjectMembership', fields ['document', 'project']
        db.create_unique(u'openn_projectmembership', ['document_id', 'project_id'])

        # Adding model 'Project'
        db.create_table(u'openn_project', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('tag', self.gf('django.db.models.fields.CharField')(default=None, unique=True, max_length=50)),
            ('name', self.gf('django.db.models.fields.CharField')(default=None, unique=True, max_length=255)),
            ('blurb', self.gf('django.db.models.fields.TextField')(default=None, null=True, blank=True)),
            ('csv_only', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('include_file', self.gf('django.db.models.fields.CharField')(default=None, max_length=255, unique=True, null=True)),
            ('live', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'openn', ['Project'])


    def backwards(self, orm):
        # Removing unique constraint on 'ProjectMembership', fields ['document', 'project']
        db.delete_unique(u'openn_projectmembership', ['document_id', 'project_id'])

        # Deleting model 'ProjectMembership'
        db.delete_table(u'openn_projectmembership')

        # Deleting model 'Project'
        db.delete_table(u'openn_project')


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
            'Meta': {'ordering': "['openn_collection', 'base_dir', 'call_number']", 'unique_together': "(('openn_collection', 'base_dir'),)", 'object_name': 'Document'},
            'base_dir': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '30'}),
            'call_number': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'collection': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '30', 'null': 'True', 'blank': 'True'}),
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
            'openn_collection': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': u"orm['openn.OPennCollection']"}),
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
        u'openn.openncollection': {
            'Meta': {'ordering': "('tag',)", 'object_name': 'OPennCollection'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'metadata_type': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '50'}),
            'tag': ('django.db.models.fields.CharField', [], {'default': 'None', 'unique': 'True', 'max_length': '50'})
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
        u'openn.project': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Project'},
            'blurb': ('django.db.models.fields.TextField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'csv_only': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'include_file': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '255', 'unique': 'True', 'null': 'True'}),
            'live': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'default': 'None', 'unique': 'True', 'max_length': '255'}),
            'tag': ('django.db.models.fields.CharField', [], {'default': 'None', 'unique': 'True', 'max_length': '50'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'openn.projectmembership': {
            'Meta': {'unique_together': "(('document', 'project'),)", 'object_name': 'ProjectMembership'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'document': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['openn.Document']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['openn.Project']"}),
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