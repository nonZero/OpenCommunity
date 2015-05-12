# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import ocd.base_models
import issues.models
import django.core.files.storage


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Issue',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('uid', models.CharField(default=ocd.base_models.create_uid, unique=True, max_length=24)),
                ('is_confidential', models.BooleanField(default=False, verbose_name='Is Confidential', editable=False)),
                ('active', models.BooleanField(default=True, verbose_name='Active')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('title', models.CharField(max_length=300, verbose_name='Title')),
                ('abstract', ocd.base_models.HTMLField(null=True, verbose_name='Background', blank=True)),
                ('content', ocd.base_models.HTMLField(null=True, verbose_name='Content', blank=True)),
                ('calculated_score', models.IntegerField(default=0, verbose_name='Calculated Score')),
                ('status', models.IntegerField(default=1, choices=[(1, 'Open'), (2, 'In upcoming meeting'), (3, 'In upcoming meeting (completed)'), (4, 'Archived')])),
                ('order_in_upcoming_meeting', models.IntegerField(default=0, null=True, verbose_name='Order in upcoming meeting', blank=True)),
                ('order_by_votes', models.FloatField(default=0, null=True, verbose_name='Order in upcoming meeting by votes', blank=True)),
                ('length_in_minutes', models.IntegerField(null=True, verbose_name='Length (in minutes)', blank=True)),
                ('completed', models.BooleanField(default=False, verbose_name='Discussion completed')),
                ('is_published', models.BooleanField(default=False, verbose_name='Is published to members')),
            ],
            options={
                'ordering': ['order_in_upcoming_meeting', 'title'],
                'verbose_name': 'Issue',
                'verbose_name_plural': 'Issues',
            },
        ),
        migrations.CreateModel(
            name='IssueAttachment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('uid', models.CharField(default=ocd.base_models.create_uid, unique=True, max_length=24)),
                ('file', models.FileField(storage=django.core.files.storage.FileSystemStorage(b'F:\\projects_with_udi\\OpenCommunity\\uploads'), upload_to=issues.models.issue_attachment_path, max_length=200, verbose_name='File')),
                ('title', models.CharField(max_length=100, verbose_name='Title')),
                ('active', models.BooleanField(default=True)),
                ('ordinal', models.PositiveIntegerField(null=True, blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='File created at')),
            ],
            options={
                'ordering': ('created_at',),
            },
        ),
        migrations.CreateModel(
            name='IssueComment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('uid', models.CharField(default=ocd.base_models.create_uid, unique=True, max_length=24)),
                ('active', models.BooleanField(default=True)),
                ('ordinal', models.PositiveIntegerField(null=True, blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('version', models.PositiveIntegerField(default=1)),
                ('last_edited_at', models.DateTimeField(auto_now_add=True, verbose_name='Last Edited at')),
                ('content', ocd.base_models.HTMLField(verbose_name='Comment')),
            ],
            options={
                'ordering': ('created_at',),
                'verbose_name': 'Issue comment',
                'verbose_name_plural': 'Issue comments',
            },
        ),
        migrations.CreateModel(
            name='IssueCommentRevision',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('version', models.PositiveIntegerField(null=True, blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('content', models.TextField(verbose_name='Content')),
            ],
        ),
        migrations.CreateModel(
            name='IssueRankingVote',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('rank', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Proposal',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('uid', models.CharField(default=ocd.base_models.create_uid, unique=True, max_length=24)),
                ('is_confidential', models.BooleanField(default=False, verbose_name='Is Confidential', editable=False)),
                ('active', models.BooleanField(default=True, verbose_name='Active')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Create at')),
                ('type', models.PositiveIntegerField(verbose_name='Type', choices=[(1, '\u05de\u05e9\u05d9\u05de\u05d4'), (2, '\u05e0\u05d5\u05d4\u05dc'), (3, '\u05db\u05dc\u05dc\u05d9')])),
                ('title', models.CharField(max_length=300, verbose_name='Title')),
                ('content', ocd.base_models.HTMLField(null=True, verbose_name='Details', blank=True)),
                ('status', models.IntegerField(default=1, choices=[(1, 'In discussion'), (2, 'Accepted'), (3, 'Rejected')])),
                ('assigned_to', models.CharField(max_length=200, null=True, verbose_name='Assigned to', blank=True)),
                ('due_by', models.DateField(null=True, verbose_name='Due by', blank=True)),
                ('task_completed', models.BooleanField(default=False, verbose_name='Completed')),
                ('votes_pro', models.PositiveIntegerField(null=True, verbose_name='Votes pro', blank=True)),
                ('votes_con', models.PositiveIntegerField(null=True, verbose_name='Votes con', blank=True)),
                ('community_members', models.PositiveIntegerField(null=True, verbose_name='Community members', blank=True)),
                ('register_board_votes', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'Proposal',
                'verbose_name_plural': 'Proposals',
            },
        ),
        migrations.CreateModel(
            name='ProposalVote',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('value', models.SmallIntegerField(default=0, verbose_name='Vote', choices=[(-1, '\u05e0\u05d2\u05d3'), (0, '\u05e0\u05de\u05e0\u05e2'), (1, '\u05d1\u05e2\u05d3')])),
            ],
            options={
                'verbose_name': 'Proposal Vote',
                'verbose_name_plural': 'Proposal Votes',
            },
        ),
        migrations.CreateModel(
            name='ProposalVoteArgument',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('argument', models.TextField(verbose_name='Argument')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Create at')),
            ],
            options={
                'verbose_name': 'Proposal vote argument',
                'verbose_name_plural': 'Proposal vote arguments',
            },
        ),
        migrations.CreateModel(
            name='ProposalVoteArgumentRanking',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('value', models.SmallIntegerField(verbose_name='Vote', choices=[(-1, '\u05e0\u05d2\u05d3'), (1, '\u05d1\u05e2\u05d3')])),
            ],
            options={
                'verbose_name': 'Proposal vote argument ranking',
                'verbose_name_plural': 'Proposal vote arguments ranking',
            },
        ),
        migrations.CreateModel(
            name='ProposalVoteBoard',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('value', models.SmallIntegerField(default=0, verbose_name='Vote', choices=[(-1, '\u05e0\u05d2\u05d3'), (0, '\u05e0\u05de\u05e0\u05e2'), (1, '\u05d1\u05e2\u05d3')])),
                ('voted_by_chairman', models.BooleanField(default=False, verbose_name='Voted by chairman')),
            ],
            options={
                'verbose_name': 'Proposal Vote',
                'verbose_name_plural': 'Proposal Votes',
            },
        ),
        migrations.CreateModel(
            name='VoteResult',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('votes_pro', models.PositiveIntegerField(verbose_name='Votes pro')),
                ('votes_con', models.PositiveIntegerField(verbose_name='Votes con')),
                ('community_members', models.PositiveIntegerField(verbose_name='Community members')),
            ],
            options={
                'verbose_name': 'Vote result',
                'verbose_name_plural': 'Vote results',
            },
        ),
    ]
