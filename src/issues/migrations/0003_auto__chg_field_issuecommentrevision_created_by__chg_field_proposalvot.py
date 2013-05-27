# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    depends_on = (
        ("users", "0002_create_users"),
    )

    def forwards(self, orm):

        # Changing field 'IssueCommentRevision.created_by'
        db.alter_column(u'issues_issuecommentrevision', 'created_by_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['users.OCUser']))

        # Changing field 'ProposalVote.user'
        db.alter_column(u'issues_proposalvote', 'user_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['users.OCUser']))

        # Changing field 'IssueComment.created_by'
        db.alter_column(u'issues_issuecomment', 'created_by_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['users.OCUser']))

        # Changing field 'IssueComment.last_edited_by'
        db.alter_column(u'issues_issuecomment', 'last_edited_by_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['users.OCUser']))

        # Changing field 'Issue.created_by'
        db.alter_column(u'issues_issue', 'created_by_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['users.OCUser']))

        # Changing field 'Proposal.created_by'
        db.alter_column(u'issues_proposal', 'created_by_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['users.OCUser']))

        # Changing field 'Proposal.assigned_to_user'
        db.alter_column(u'issues_proposal', 'assigned_to_user_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['users.OCUser']))

    def backwards(self, orm):

        # Changing field 'IssueCommentRevision.created_by'
        db.alter_column(u'issues_issuecommentrevision', 'created_by_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User']))

        # Changing field 'ProposalVote.user'
        db.alter_column(u'issues_proposalvote', 'user_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User']))

        # Changing field 'IssueComment.created_by'
        db.alter_column(u'issues_issuecomment', 'created_by_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User']))

        # Changing field 'IssueComment.last_edited_by'
        db.alter_column(u'issues_issuecomment', 'last_edited_by_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['auth.User']))

        # Changing field 'Issue.created_by'
        db.alter_column(u'issues_issue', 'created_by_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User']))

        # Changing field 'Proposal.created_by'
        db.alter_column(u'issues_proposal', 'created_by_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User']))

        # Changing field 'Proposal.assigned_to_user'
        db.alter_column(u'issues_proposal', 'assigned_to_user_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['auth.User']))

    models = {
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
        u'communities.community': {
            'Meta': {'object_name': 'Community'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'members': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'communities'", 'blank': 'True', 'through': u"orm['communities.CommunityMember']", 'to': u"orm['users.OCUser']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'upcoming_meeting_comments': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'upcoming_meeting_is_published': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'upcoming_meeting_location': ('django.db.models.fields.CharField', [], {'max_length': '300', 'null': 'True', 'blank': 'True'}),
            'upcoming_meeting_participants': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'+'", 'blank': 'True', 'to': u"orm['users.OCUser']"}),
            'upcoming_meeting_published_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'upcoming_meeting_scheduled_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'upcoming_meeting_version': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        u'communities.communitymember': {
            'Meta': {'unique_together': "(('community', 'user'),)", 'object_name': 'CommunityMember'},
            'community': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['communities.Community']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_chairman': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_in_board': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_secretary': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['users.OCUser']"})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'issues.issue': {
            'Meta': {'object_name': 'Issue'},
            'abstract': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'calculated_score': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'closed_at_meeting': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['meetings.Meeting']", 'null': 'True', 'blank': 'True'}),
            'community': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'issues'", 'to': u"orm['communities.Community']"}),
            'content': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'issues_created'", 'to': u"orm['users.OCUser']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'in_upcoming_meeting': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_closed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '300'})
        },
        u'issues.issuecomment': {
            'Meta': {'ordering': "('created_at',)", 'object_name': 'IssueComment'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'content': ('django.db.models.fields.TextField', [], {}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'issue_comments_created'", 'to': u"orm['users.OCUser']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'issue': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'comments'", 'to': u"orm['issues.Issue']"}),
            'last_edited_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'last_edited_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'issue_comments_last_edited'", 'null': 'True', 'to': u"orm['users.OCUser']"}),
            'ordinal': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'version': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1'})
        },
        u'issues.issuecommentrevision': {
            'Meta': {'object_name': 'IssueCommentRevision'},
            'comment': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'revisions'", 'to': u"orm['issues.IssueComment']"}),
            'content': ('django.db.models.fields.TextField', [], {}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'issue_comment_versions_created'", 'to': u"orm['users.OCUser']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'version': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        u'issues.proposal': {
            'Meta': {'object_name': 'Proposal'},
            'accepted_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'assigned_to': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'assigned_to_user': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'proposals_assigned'", 'null': 'True', 'to': u"orm['users.OCUser']"}),
            'content': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'proposals_created'", 'to': u"orm['users.OCUser']"}),
            'due_by': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_accepted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'issue': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'proposals'", 'to': u"orm['issues.Issue']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'type': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'votes': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'proposals'", 'blank': 'True', 'through': u"orm['issues.ProposalVote']", 'to': u"orm['users.OCUser']"})
        },
        u'issues.proposalvote': {
            'Meta': {'unique_together': "(('proposal', 'user'),)", 'object_name': 'ProposalVote'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'proposal': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['issues.Proposal']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['users.OCUser']"}),
            'value': ('django.db.models.fields.PositiveIntegerField', [], {})
        },
        u'meetings.agendaitem': {
            'Meta': {'unique_together': "(('meeting', 'issue'),)", 'object_name': 'AgendaItem'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'issue': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['issues.Issue']"}),
            'meeting': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['meetings.Meeting']"}),
            'order': ('django.db.models.fields.PositiveIntegerField', [], {'default': '100'})
        },
        u'meetings.meeting': {
            'Meta': {'ordering': "('-held_at',)", 'object_name': 'Meeting'},
            'agenda_items': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['issues.Issue']", 'symmetrical': 'False', 'through': u"orm['meetings.AgendaItem']", 'blank': 'True'}),
            'comments': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'community': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'meetings'", 'to': u"orm['communities.Community']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'meetings_created'", 'to': u"orm['users.OCUser']"}),
            'held_at': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '300', 'null': 'True', 'blank': 'True'}),
            'participants': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'participated_in_meeting'", 'symmetrical': 'False', 'to': u"orm['users.OCUser']"}),
            'scheduled_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'summary': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        },
        u'users.ocuser': {
            'Meta': {'object_name': 'OCUser'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'display_name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '255', 'db_index': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        }
    }

    complete_apps = ['issues']