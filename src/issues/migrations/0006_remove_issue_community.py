# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('issues', '0005_auto_20150513_1232'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='issue',
            name='community',
        ),
    ]
