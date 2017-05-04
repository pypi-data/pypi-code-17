# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Progress'
        db.create_table('djprogress_progress', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=64, db_index=True)),
            ('current', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('total', self.gf('django.db.models.fields.IntegerField')(default=100)),
            ('eta', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('last_updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, db_index=True, blank=True)),
        ))
        db.send_create_signal('djprogress', ['Progress'])


    def backwards(self, orm):
        
        # Deleting model 'Progress'
        db.delete_table('djprogress_progress')


    models = {
        'djprogress.progress': {
            'Meta': {'object_name': 'Progress'},
            'current': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'eta': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'db_index': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64', 'db_index': 'True'}),
            'total': ('django.db.models.fields.IntegerField', [], {'default': '100'})
        }
    }

    complete_apps = ['djprogress']
