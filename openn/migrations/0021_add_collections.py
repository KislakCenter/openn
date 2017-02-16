# -*- coding: utf-8 -*-
import os
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models
from django.conf import settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "openn.settings")

class Migration(DataMigration):

    def find_or_create(self, orm, tag):
        attrs = { 'tag': tag }
        try:
            coll = orm.OPennCollection.objects.get(**attrs)
            print "Found collection: %s" % (coll.tag,)
        except orm.OPennCollection.DoesNotExist:
            coll = orm.OPennCollection(tag = tag)
            print "Creating collection: %s" % (coll.tag,)
            coll.save()

        return coll

    def forwards(self, orm):
        "Write your forwards methods here."
        # Note: Don't use "from appname.models import ModelName".
        # Use orm.ModelName to refer to models in this application,
        # and orm['appname.ModelName'] for models in other applications.

        # first do Penn and LJS
        for tag in ( 'ljs', 'pennmss' ):
            self.find_or_create(orm, tag)

        # Now do any others
        for config in settings.REPOSITORIES['configs']:
            tag = config['tag']
            self.find_or_create(orm, tag)

    def backwards(self, orm):
        "Write your backwards methods here."
        orm.OPennCollection.objects.all().delete()

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
            'openn_collection': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': u"orm['openn.OPennCollection']", 'null': 'True', 'blank': 'True'}),
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
    symmetrical = True
