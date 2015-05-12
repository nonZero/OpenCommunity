# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('meetings', '0002_auto_20150512_1238'),
        ('issues', '0002_auto_20150512_1238'),
        ('communities', '0002_auto_20150512_1238'),
    ]

    operations = [
        migrations.AddField(
            model_name='proposalvoteboard',
            name='user',
            field=models.ForeignKey(related_name='board_votes', verbose_name='User', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='proposalvoteargumentranking',
            name='argument',
            field=models.ForeignKey(to='issues.ProposalVoteArgument'),
        ),
        migrations.AddField(
            model_name='proposalvoteargumentranking',
            name='user',
            field=models.ForeignKey(related_name='argument_votes', verbose_name='User', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='proposalvoteargument',
            name='created_by',
            field=models.ForeignKey(related_name='arguments_created', verbose_name='Created by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='proposalvoteargument',
            name='proposal_vote',
            field=models.ForeignKey(related_name='arguments', to='issues.ProposalVote'),
        ),
        migrations.AddField(
            model_name='proposalvote',
            name='proposal',
            field=models.ForeignKey(related_name='votes', to='issues.Proposal'),
        ),
        migrations.AddField(
            model_name='proposalvote',
            name='user',
            field=models.ForeignKey(related_name='votes', verbose_name='User', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='proposal',
            name='assigned_to_user',
            field=models.ForeignKey(related_name='proposals_assigned', verbose_name='Assigned to user', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='proposal',
            name='confidential_reason',
            field=models.ForeignKey(blank=True, to='communities.CommunityConfidentialReason', null=True),
        ),
        migrations.AddField(
            model_name='proposal',
            name='created_by',
            field=models.ForeignKey(related_name='proposals_created', verbose_name='Created by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='proposal',
            name='decided_at_meeting',
            field=models.ForeignKey(blank=True, to='meetings.Meeting', null=True),
        ),
        migrations.AddField(
            model_name='proposal',
            name='issue',
            field=models.ForeignKey(related_name='proposals', to='issues.Issue'),
        ),
        migrations.AddField(
            model_name='proposal',
            name='tags',
            field=taggit.managers.TaggableManager(to='taggit.Tag', through='taggit.TaggedItem', blank=True, help_text='A comma-separated list of tags.', verbose_name='Tags'),
        ),
        migrations.AddField(
            model_name='issuerankingvote',
            name='issue',
            field=models.ForeignKey(related_name='ranking_votes', to='issues.Issue'),
        ),
        migrations.AddField(
            model_name='issuerankingvote',
            name='voted_by',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='issuecommentrevision',
            name='comment',
            field=models.ForeignKey(related_name='revisions', to='issues.IssueComment'),
        ),
        migrations.AddField(
            model_name='issuecommentrevision',
            name='created_by',
            field=models.ForeignKey(related_name='issue_comment_versions_created', verbose_name='Created by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='issuecomment',
            name='created_by',
            field=models.ForeignKey(related_name='issue_comments_created', verbose_name='Created by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='issuecomment',
            name='issue',
            field=models.ForeignKey(related_name='comments', to='issues.Issue'),
        ),
        migrations.AddField(
            model_name='issuecomment',
            name='last_edited_by',
            field=models.ForeignKey(related_name='issue_comments_last_edited', verbose_name='Created by', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='issuecomment',
            name='meeting',
            field=models.ForeignKey(blank=True, to='meetings.Meeting', null=True),
        ),
        migrations.AddField(
            model_name='issueattachment',
            name='agenda_item',
            field=models.ForeignKey(related_name='attachments', blank=True, to='meetings.AgendaItem', null=True),
        ),
        migrations.AddField(
            model_name='issueattachment',
            name='created_by',
            field=models.ForeignKey(related_name='files_created', verbose_name='Created by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='issueattachment',
            name='issue',
            field=models.ForeignKey(related_name='attachments', to='issues.Issue'),
        ),
        migrations.AddField(
            model_name='issue',
            name='community',
            field=models.ForeignKey(related_name='issues', to='communities.Community'),
        ),
        migrations.AddField(
            model_name='issue',
            name='confidential_reason',
            field=models.ForeignKey(blank=True, to='communities.CommunityConfidentialReason', null=True),
        ),
        migrations.AddField(
            model_name='issue',
            name='created_by',
            field=models.ForeignKey(related_name='issues_created', verbose_name='Created by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='voteresult',
            unique_together=set([('proposal', 'meeting')]),
        ),
        migrations.AlterUniqueTogether(
            name='proposalvoteboard',
            unique_together=set([('proposal', 'user')]),
        ),
        migrations.AlterUniqueTogether(
            name='proposalvote',
            unique_together=set([('proposal', 'user')]),
        ),
    ]
