# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('communities', '0004_auto_20150513_1023'),
    ]

    operations = [
        migrations.AddField(
            model_name='community',
            name='slug',
            field=models.SlugField(max_length=200, null=True, verbose_name=b'Friendly URL', blank=True),
        ),
    ]
