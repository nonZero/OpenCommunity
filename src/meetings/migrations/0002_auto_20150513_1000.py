# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('meetings', '0001_initial'),
        ('issues', '0002_auto_20150513_1000'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('communities', '0002_auto_20150513_1000'),
    ]

    operations = [
        migrations.AddField(
            model_name='meetingparticipant',
            name='user',
            field=models.ForeignKey(related_name='participations', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='meetingexternalparticipant',
            name='meeting',
            field=models.ForeignKey(verbose_name='Meeting', to='meetings.Meeting'),
        ),
        migrations.AddField(
            model_name='meeting',
            name='agenda_items',
            field=models.ManyToManyField(related_name='meetings', verbose_name='Agenda items', to='issues.Issue', through='meetings.AgendaItem', blank=True),
        ),
        migrations.AddField(
            model_name='meeting',
            name='community',
            field=models.ForeignKey(related_name='meetings', verbose_name='Community', to='communities.Community'),
        ),
        migrations.AddField(
            model_name='meeting',
            name='created_by',
            field=models.ForeignKey(related_name='meetings_created', verbose_name='Created by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='meeting',
            name='participants',
            field=models.ManyToManyField(related_name='participated_in_meeting', verbose_name='Participants', through='meetings.MeetingParticipant', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='agendaitem',
            name='issue',
            field=models.ForeignKey(related_name='agenda_items', verbose_name='Issue', to='issues.Issue'),
        ),
        migrations.AddField(
            model_name='agendaitem',
            name='meeting',
            field=models.ForeignKey(related_name='agenda', verbose_name='Meeting', to='meetings.Meeting'),
        ),
        migrations.AlterUniqueTogether(
            name='meetingparticipant',
            unique_together=set([('meeting', 'user'), ('meeting', 'ordinal')]),
        ),
        migrations.AlterUniqueTogether(
            name='agendaitem',
            unique_together=set([('meeting', 'issue')]),
        ),
    ]
