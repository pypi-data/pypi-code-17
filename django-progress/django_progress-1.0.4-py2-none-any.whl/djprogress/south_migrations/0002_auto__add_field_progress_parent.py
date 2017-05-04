# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'Progress.parent'
        db.add_column('djprogress_progress', 'parent', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='children', null=True, to=orm['djprogress.Progress']), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'Progress.parent'
        db.delete_column('djprogress_progress', 'parent_id')


    models = {
        'djprogress.progress': {
            'Meta': {'object_name': 'Progress'},
            'current': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'eta': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'db_index': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64', 'db_index': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': "orm['djprogress.Progress']"}),
            'total': ('django.db.models.fields.IntegerField', [], {'default': '100'})
        }
    }

    complete_apps = ['djprogress']
