# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0011_auto_20150621_1334'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='invitation',
            name='group_role',
        ),
        migrations.AlterField(
            model_name='membership',
            name='default_group_name',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Old group', choices=[(b'member', 'member'), (b'board', 'board'), (b'secretary', 'secretary'), (b'chairman', 'chairman')]),
        ),
    ]
