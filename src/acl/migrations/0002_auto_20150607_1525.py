# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('acl', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='role',
            name='community',
            field=models.ForeignKey(related_name='roles', verbose_name='Limit to community', blank=True, to='communities.Community', null=True),
        ),
        migrations.AlterField(
            model_name='role',
            name='title',
            field=models.CharField(max_length=200, verbose_name='title'),
        ),
        migrations.AlterUniqueTogether(
            name='role',
            unique_together=set([('community', 'title')]),
        ),
    ]
