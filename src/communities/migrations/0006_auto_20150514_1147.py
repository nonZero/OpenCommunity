# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('communities', '0005_community_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='committee',
            name='logo',
            field=models.ImageField(upload_to=b'committee_logo', null=True, verbose_name='Committee logo', blank=True),
        ),
        migrations.AlterField(
            model_name='committee',
            name='official_identifier',
            field=models.CharField(max_length=300, null=True, verbose_name='Committee identifier', blank=True),
        ),
    ]
