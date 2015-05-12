# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('communities', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='community',
            name='upcoming_meeting_participants',
            field=models.ManyToManyField(related_name='+', verbose_name='Participants in upcoming meeting', to=settings.AUTH_USER_MODEL, blank=True),
        ),
        migrations.AlterUniqueTogether(
            name='communityconfidentialreason',
            unique_together=set([('community', 'title')]),
        ),
    ]
