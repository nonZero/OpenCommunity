# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('meetings', '0004_auto_20150513_1232'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='meeting',
            name='community',
        ),
    ]
