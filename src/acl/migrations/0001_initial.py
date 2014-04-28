# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Role'
        db.create_table(u'acl_role', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('ordinal', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('title', self.gf('django.db.models.fields.CharField')(unique=True, max_length=200)),
            ('based_on', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
        ))
        db.send_create_signal(u'acl', ['Role'])

        # Adding model 'RolePermission'
        db.create_table(u'acl_rolepermission', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('role', self.gf('django.db.models.fields.related.ForeignKey')(related_name='perms', to=orm['acl.Role'])),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal(u'acl', ['RolePermission'])

        # Adding unique constraint on 'RolePermission', fields ['role', 'code']
        db.create_unique(u'acl_rolepermission', ['role_id', 'code'])


    def backwards(self, orm):
        # Removing unique constraint on 'RolePermission', fields ['role', 'code']
        db.delete_unique(u'acl_rolepermission', ['role_id', 'code'])

        # Deleting model 'Role'
        db.delete_table(u'acl_role')

        # Deleting model 'RolePermission'
        db.delete_table(u'acl_rolepermission')


    models = {
        u'acl.role': {
            'Meta': {'object_name': 'Role'},
            'based_on': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ordinal': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'title': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'})
        },
        u'acl.rolepermission': {
            'Meta': {'unique_together': "(('role', 'code'),)", 'object_name': 'RolePermission'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'role': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'perms'", 'to': u"orm['acl.Role']"})
        }
    }

    complete_apps = ['acl']