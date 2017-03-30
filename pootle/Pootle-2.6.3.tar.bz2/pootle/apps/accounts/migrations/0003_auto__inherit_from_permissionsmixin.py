# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import connection, models


class Migration(SchemaMigration):
    depends_on = (
        ("pootle_app", "0006_auto__del_suggestion"),
    )

    def forwards(self, orm):
        # Adding M2M table for field groups on 'User'
        old_m2m_table_name = db.shorten_name(u'auth_user_groups')
        m2m_table_name = db.shorten_name(u'accounts_user_groups')
        if old_m2m_table_name in connection.introspection.table_names():
            print("Renaming %r to %r" % (old_m2m_table_name, m2m_table_name))
            db.rename_table(old_m2m_table_name, m2m_table_name)
        else:
            print("%r does not exist. Creating table %r instead" % (old_m2m_table_name, m2m_table_name))
            db.create_table(m2m_table_name, (
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
                ('user', models.ForeignKey(orm[u'accounts.user'], null=False)),
                ('group', models.ForeignKey(orm[u'auth.group'], null=False))
            ))
            print("Creating unique between %r.user_id<->%r.group_id" % (m2m_table_name, m2m_table_name))
            db.create_unique(m2m_table_name, ['user_id', 'group_id'])

        # Adding M2M table for field user_permissions on 'User'
        old_m2m_table_name = db.shorten_name(u'auth_user_user_permissions')
        m2m_table_name = db.shorten_name(u'accounts_user_user_permissions')
        if old_m2m_table_name in connection.introspection.table_names():
            print("Renaming %r to %r" % (old_m2m_table_name, m2m_table_name))
            db.rename_table(old_m2m_table_name, m2m_table_name)
        else:
            print("%r does not exist. Creating table %r instead" % (old_m2m_table_name, m2m_table_name))
            db.create_table(m2m_table_name, (
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
                ('user', models.ForeignKey(orm[u'accounts.user'], null=False)),
                ('permission', models.ForeignKey(orm[u'auth.permission'], null=False))
            ))
            print("Creating unique between %r.user_id<->%r.permission_id" % (m2m_table_name, m2m_table_name))
            db.create_unique(m2m_table_name, ['user_id', 'permission_id'])

    def backwards(self, orm):
        raise RuntimeError("Cannot reverse this migration.")

    models = {
        u'accounts.user': {
            'Meta': {'object_name': 'User'},
            '_unit_rows': ('django.db.models.fields.SmallIntegerField', [], {'default': '9', 'db_column': "'unit_rows'"}),
            'alt_src_langs': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'user_alt_src_langs'", 'blank': 'True', 'db_index': 'True', 'to': u"orm['pootle_language.Language']"}),
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '255'}),
            'full_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'pootle_app.directory': {
            'Meta': {'ordering': "['name']", 'object_name': 'Directory'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'child_dirs'", 'null': 'True', 'to': "orm['pootle_app.Directory']"}),
            'pootle_path': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'})
        },
        u'pootle_language.language': {
            'Meta': {'ordering': "['code']", 'object_name': 'Language', 'db_table': "'pootle_app_language'"},
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50', 'db_index': 'True'}),
            'description': ('pootle.core.markup.fields.MarkupField', [], {'blank': 'True'}),
            'directory': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['pootle_app.Directory']", 'unique': 'True'}),
            'fullname': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nplurals': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'}),
            'pluralequation': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'specialchars': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'})
        }
    }

    complete_apps = ['accounts']
