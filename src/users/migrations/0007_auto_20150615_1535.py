# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_auto_20150615_1421'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invitation',
            name='default_group_name',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Group', choices=[(b'member', 'member'), (b'board', 'board'), (b'secretary', 'secretary'), (b'chairman', 'chairman')]),
        ),
    ]
