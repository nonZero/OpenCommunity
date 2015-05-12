# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import ocd.base_models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Community',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('uid', models.CharField(default=ocd.base_models.create_uid, unique=True, max_length=24)),
                ('name', models.CharField(max_length=200, verbose_name='Name')),
                ('is_public', models.BooleanField(default=False, db_index=True, verbose_name='Public community')),
                ('logo', models.ImageField(upload_to=b'community_logo', null=True, verbose_name='Community logo', blank=True)),
                ('official_identifier', models.CharField(max_length=300, null=True, verbose_name='Community identifier', blank=True)),
                ('upcoming_meeting_started', models.BooleanField(default=False, verbose_name='Meeting started')),
                ('upcoming_meeting_title', models.CharField(max_length=300, null=True, verbose_name='Upcoming meeting title', blank=True)),
                ('upcoming_meeting_scheduled_at', models.DateTimeField(null=True, verbose_name='Upcoming meeting scheduled at', blank=True)),
                ('upcoming_meeting_location', models.CharField(max_length=300, null=True, verbose_name='Upcoming meeting location', blank=True)),
                ('upcoming_meeting_comments', ocd.base_models.HTMLField(null=True, verbose_name='Upcoming meeting background', blank=True)),
                ('upcoming_meeting_guests', models.TextField(help_text='Enter each guest in a separate line', null=True, verbose_name='Guests in upcoming meeting', blank=True)),
                ('upcoming_meeting_version', models.IntegerField(default=0, verbose_name='Upcoming meeting version')),
                ('upcoming_meeting_is_published', models.BooleanField(default=False, verbose_name='Upcoming meeting is published')),
                ('upcoming_meeting_published_at', models.DateTimeField(null=True, verbose_name='Upcoming meeting published at', blank=True)),
                ('upcoming_meeting_summary', ocd.base_models.HTMLField(null=True, verbose_name='Upcoming meeting summary', blank=True)),
                ('board_name', models.CharField(default='Board', max_length=200, verbose_name='Board name')),
                ('straw_voting_enabled', models.BooleanField(default=False, verbose_name='Straw voting enabled')),
                ('issue_ranking_enabled', models.BooleanField(default=False, verbose_name='Issue ranking votes enabled')),
                ('voting_ends_at', models.DateTimeField(null=True, verbose_name='Straw Vote ends at', blank=True)),
                ('referendum_started', models.BooleanField(default=False, verbose_name='Referendum started')),
                ('referendum_started_at', models.DateTimeField(null=True, verbose_name='Referendum started at', blank=True)),
                ('referendum_ends_at', models.DateTimeField(null=True, verbose_name='Referendum ends at', blank=True)),
                ('default_quorum', models.PositiveSmallIntegerField(null=True, verbose_name='Default quorum', blank=True)),
                ('allow_links_in_emails', models.BooleanField(default=True, verbose_name='Allow links inside emails')),
                ('email_invitees', models.BooleanField(default=False, verbose_name='Send mails to invitees')),
                ('register_missing_board_members', models.BooleanField(default=False, verbose_name='Register missing board members')),
                ('inform_system_manager', models.BooleanField(default=False, verbose_name='Inform System Manager')),
                ('no_meetings_community', models.BooleanField(default=False, verbose_name='Community without meetings?')),
            ],
            options={
                'verbose_name': 'Community',
                'verbose_name_plural': 'Communities',
            },
        ),
        migrations.CreateModel(
            name='CommunityConfidentialReason',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(help_text='The title to give this reason.', max_length=255, verbose_name='Name')),
                ('community', models.ForeignKey(related_name='confidential_reasons', to='communities.Community', help_text='A reason that can be used for marking items as confidential in your community.')),
            ],
            options={
                'ordering': ['community'],
                'verbose_name': 'Confidential Reason',
                'verbose_name_plural': 'Confidential Reasons',
            },
        ),
    ]
