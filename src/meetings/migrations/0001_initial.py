# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import ocd.base_models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AgendaItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_confidential', models.BooleanField(default=False, verbose_name='Is Confidential', editable=False)),
                ('background', ocd.base_models.HTMLField(null=True, verbose_name='Background', blank=True)),
                ('order', models.PositiveIntegerField(default=100, verbose_name='Order')),
                ('closed', models.BooleanField(default=True, verbose_name='Closed')),
            ],
            options={
                'ordering': ('meeting__created_at', 'order'),
                'verbose_name': 'Agenda Item',
                'verbose_name_plural': 'Agenda Items',
            },
        ),
        migrations.CreateModel(
            name='Meeting',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('uid', models.CharField(default=ocd.base_models.create_uid, unique=True, max_length=24)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('held_at', models.DateTimeField(verbose_name='Held at')),
                ('title', models.CharField(max_length=300, null=True, verbose_name='Title', blank=True)),
                ('scheduled_at', models.DateTimeField(null=True, verbose_name='Scheduled at', blank=True)),
                ('location', models.CharField(max_length=300, null=True, verbose_name='Location', blank=True)),
                ('comments', models.TextField(null=True, verbose_name='Comments', blank=True)),
                ('summary', models.TextField(null=True, verbose_name='Summary', blank=True)),
                ('guests', models.TextField(help_text='Enter each guest in a separate line', null=True, verbose_name='Guests', blank=True)),
            ],
            options={
                'ordering': ('-held_at',),
                'verbose_name': 'Meeting',
                'verbose_name_plural': 'Meetings',
            },
        ),
        migrations.CreateModel(
            name='MeetingExternalParticipant',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200, verbose_name='Name')),
            ],
            options={
                'verbose_name': 'Meeting External Participant',
                'verbose_name_plural': 'Meeting External Participants',
            },
        ),
        migrations.CreateModel(
            name='MeetingParticipant',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ordinal', models.PositiveIntegerField()),
                ('display_name', models.CharField(max_length=200, verbose_name='Name')),
                ('default_group_name', models.CharField(blank=True, max_length=50, null=True, verbose_name='Group', choices=[(b'member', 'member'), (b'board', 'board'), (b'secretary', 'secretary'), (b'chairman', 'chairman')])),
                ('is_absent', models.BooleanField(default=False, verbose_name='Is Absent')),
                ('meeting', models.ForeignKey(related_name='participations', verbose_name='Meeting', to='meetings.Meeting')),
            ],
            options={
                'verbose_name': 'Meeting Participant',
                'verbose_name_plural': 'Meeting Participants',
            },
        ),
    ]
