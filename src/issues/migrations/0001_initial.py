# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    depends_on = (
        ("meetings", "0001_initial"),
    )

    def forwards(self, orm):
        # Adding model 'Issue'
        db.create_table(u'issues_issue', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('community', self.gf('django.db.models.fields.related.ForeignKey')(related_name='issues', to=orm['communities.Community'])),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('created_by', self.gf('django.db.models.fields.related.ForeignKey')(related_name='issues_created', to=orm['users.OCUser'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=300)),
            ('abstract', self.gf('ocd.base_models.HTMLField')(null=True, blank=True)),
            ('content', self.gf('ocd.base_models.HTMLField')(null=True, blank=True)),
            ('calculated_score', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('in_upcoming_meeting', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('order_in_upcoming_meeting', self.gf('django.db.models.fields.IntegerField')(default=9999, null=True, blank=True)),
            ('length_in_minutes', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('is_closed', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('closed_at_meeting', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['meetings.Meeting'], null=True, blank=True)),
        ))
        db.send_create_signal(u'issues', ['Issue'])

        # Adding model 'IssueComment'
        db.create_table(u'issues_issuecomment', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('issue', self.gf('django.db.models.fields.related.ForeignKey')(related_name='comments', to=orm['issues.Issue'])),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('ordinal', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('created_by', self.gf('django.db.models.fields.related.ForeignKey')(related_name='issue_comments_created', to=orm['users.OCUser'])),
            ('version', self.gf('django.db.models.fields.PositiveIntegerField')(default=1)),
            ('last_edited_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('last_edited_by', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='issue_comments_last_edited', null=True, to=orm['users.OCUser'])),
            ('content', self.gf('ocd.base_models.HTMLField')()),
        ))
        db.send_create_signal(u'issues', ['IssueComment'])

        # Adding model 'IssueCommentRevision'
        db.create_table(u'issues_issuecommentrevision', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('comment', self.gf('django.db.models.fields.related.ForeignKey')(related_name='revisions', to=orm['issues.IssueComment'])),
            ('version', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('created_by', self.gf('django.db.models.fields.related.ForeignKey')(related_name='issue_comment_versions_created', to=orm['users.OCUser'])),
            ('content', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'issues', ['IssueCommentRevision'])

        # Adding model 'ProposalVote'
        db.create_table(u'issues_proposalvote', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('proposal', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['issues.Proposal'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['users.OCUser'])),
            ('value', self.gf('django.db.models.fields.PositiveIntegerField')()),
        ))
        db.send_create_signal(u'issues', ['ProposalVote'])

        # Adding unique constraint on 'ProposalVote', fields ['proposal', 'user']
        db.create_unique(u'issues_proposalvote', ['proposal_id', 'user_id'])

        # Adding model 'Proposal'
        db.create_table(u'issues_proposal', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('issue', self.gf('django.db.models.fields.related.ForeignKey')(related_name='proposals', to=orm['issues.Issue'])),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('created_by', self.gf('django.db.models.fields.related.ForeignKey')(related_name='proposals_created', to=orm['users.OCUser'])),
            ('type', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=300)),
            ('content', self.gf('ocd.base_models.HTMLField')(null=True, blank=True)),
            ('is_accepted', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('accepted_at', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('assigned_to', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('assigned_to_user', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='proposals_assigned', null=True, to=orm['users.OCUser'])),
            ('due_by', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'issues', ['Proposal'])


    def backwards(self, orm):
        # Removing unique constraint on 'ProposalVote', fields ['proposal', 'user']
        db.delete_unique(u'issues_proposalvote', ['proposal_id', 'user_id'])

        # Deleting model 'Issue'
        db.delete_table(u'issues_issue')

        # Deleting model 'IssueComment'
        db.delete_table(u'issues_issuecomment')

        # Deleting model 'IssueCommentRevision'
        db.delete_table(u'issues_issuecommentrevision')

        # Deleting model 'ProposalVote'
        db.delete_table(u'issues_proposalvote')

        # Deleting model 'Proposal'
        db.delete_table(u'issues_proposal')


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
            'board_name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'upcoming_meeting_comments': ('ocd.base_models.HTMLField', [], {'null': 'True', 'blank': 'True'}),
            'upcoming_meeting_guests': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'upcoming_meeting_is_published': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'upcoming_meeting_location': ('django.db.models.fields.CharField', [], {'max_length': '300', 'null': 'True', 'blank': 'True'}),
            'upcoming_meeting_participants': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'+'", 'blank': 'True', 'to': u"orm['users.OCUser']"}),
            'upcoming_meeting_published_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'upcoming_meeting_scheduled_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'upcoming_meeting_started': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'upcoming_meeting_summary': ('ocd.base_models.HTMLField', [], {'null': 'True', 'blank': 'True'}),
            'upcoming_meeting_version': ('django.db.models.fields.IntegerField', [], {'default': '0'})
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
            'abstract': ('ocd.base_models.HTMLField', [], {'null': 'True', 'blank': 'True'}),
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'calculated_score': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'closed_at_meeting': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['meetings.Meeting']", 'null': 'True', 'blank': 'True'}),
            'community': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'issues'", 'to': u"orm['communities.Community']"}),
            'content': ('ocd.base_models.HTMLField', [], {'null': 'True', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'issues_created'", 'to': u"orm['users.OCUser']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'in_upcoming_meeting': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_closed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'length_in_minutes': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'order_in_upcoming_meeting': ('django.db.models.fields.IntegerField', [], {'default': '9999', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '300'})
        },
        u'issues.issuecomment': {
            'Meta': {'ordering': "('created_at',)", 'object_name': 'IssueComment'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'content': ('ocd.base_models.HTMLField', [], {}),
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
            'content': ('ocd.base_models.HTMLField', [], {'null': 'True', 'blank': 'True'}),
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
            'closed': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'issue': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['issues.Issue']"}),
            'meeting': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'agenda'", 'to': u"orm['meetings.Meeting']"}),
            'order': ('django.db.models.fields.PositiveIntegerField', [], {'default': '100'})
        },
        u'meetings.meeting': {
            'Meta': {'ordering': "('-held_at',)", 'object_name': 'Meeting'},
            'agenda_items': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['issues.Issue']", 'symmetrical': 'False', 'through': u"orm['meetings.AgendaItem']", 'blank': 'True'}),
            'comments': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'community': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'meetings'", 'to': u"orm['communities.Community']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'meetings_created'", 'to': u"orm['users.OCUser']"}),
            'guests': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'held_at': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '300', 'null': 'True', 'blank': 'True'}),
            'participants': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'participated_in_meeting'", 'symmetrical': 'False', 'through': u"orm['meetings.MeetingParticipant']", 'to': u"orm['users.OCUser']"}),
            'scheduled_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'summary': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        },
        u'meetings.meetingparticipant': {
            'Meta': {'unique_together': "(('meeting', 'ordinal'), ('meeting', 'user'))", 'object_name': 'MeetingParticipant'},
            'default_group_name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'display_name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'meeting': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'participations'", 'to': u"orm['meetings.Meeting']"}),
            'ordinal': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'participations'", 'to': u"orm['users.OCUser']"})
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