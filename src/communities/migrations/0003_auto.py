# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Removing M2M table for field upcoming_meeting_participants on 'Community'
        db.delete_table('communities_community_upcoming_meeting_participants')


    def backwards(self, orm):
        # Adding M2M table for field upcoming_meeting_participants on 'Community'
        db.create_table(u'communities_community_upcoming_meeting_participants', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('community', models.ForeignKey(orm[u'communities.community'], null=False)),
            ('ocuser', models.ForeignKey(orm[u'users.ocuser'], null=False))
        ))
        db.create_unique(u'communities_community_upcoming_meeting_participants', ['community_id', 'ocuser_id'])


    models = {
        u'communities.community': {
            'Meta': {'object_name': 'Community'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'upcoming_meeting_comments': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'upcoming_meeting_is_published': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'upcoming_meeting_location': ('django.db.models.fields.CharField', [], {'max_length': '300', 'null': 'True', 'blank': 'True'}),
            'upcoming_meeting_published_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'upcoming_meeting_scheduled_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'upcoming_meeting_version': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        }
    }

    complete_apps = ['communities']