# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('communities', '0006_auto_20150514_1147'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='committee',
            name='board_name',
        ),
        migrations.RemoveField(
            model_name='committee',
            name='no_meetings_community',
        ),
        migrations.RemoveField(
            model_name='community',
            name='board_name',
        ),
        migrations.RemoveField(
            model_name='community',
            name='upcoming_meeting_comments',
        ),
        migrations.RemoveField(
            model_name='community',
            name='upcoming_meeting_guests',
        ),
        migrations.RemoveField(
            model_name='community',
            name='upcoming_meeting_is_published',
        ),
        migrations.RemoveField(
            model_name='community',
            name='upcoming_meeting_location',
        ),
        migrations.RemoveField(
            model_name='community',
            name='upcoming_meeting_participants',
        ),
        migrations.RemoveField(
            model_name='community',
            name='upcoming_meeting_published_at',
        ),
        migrations.RemoveField(
            model_name='community',
            name='upcoming_meeting_scheduled_at',
        ),
        migrations.RemoveField(
            model_name='community',
            name='upcoming_meeting_started',
        ),
        migrations.RemoveField(
            model_name='community',
            name='upcoming_meeting_summary',
        ),
        migrations.RemoveField(
            model_name='community',
            name='upcoming_meeting_title',
        ),
        migrations.RemoveField(
            model_name='community',
            name='upcoming_meeting_version',
        ),
        migrations.AddField(
            model_name='committee',
            name='no_meetings_committee',
            field=models.BooleanField(default=False, verbose_name='Committee without meetings?'),
        ),
        migrations.AlterField(
            model_name='committee',
            name='community',
            field=models.ForeignKey(related_name='committees', verbose_name='Community', to='communities.Community', null=True),
        ),
    ]
