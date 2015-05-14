# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('communities', '0004_auto_20150513_1023'),
        ('issues', '0003_auto_20150513_1000'),
    ]

    operations = [
        migrations.AddField(
            model_name='issue',
            name='committee',
            field=models.ForeignKey(related_name='issues', to='communities.Committee', null=True),
        ),
    ]
