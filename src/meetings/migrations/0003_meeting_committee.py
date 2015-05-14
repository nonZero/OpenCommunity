# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('communities', '0004_auto_20150513_1023'),
        ('meetings', '0002_auto_20150513_1000'),
    ]

    operations = [
        migrations.AddField(
            model_name='meeting',
            name='committee',
            field=models.ForeignKey(related_name='meetings', verbose_name='Committee', to='communities.Committee', null=True),
        ),
    ]
