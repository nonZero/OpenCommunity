# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('acl', '0002_auto_20150607_1525'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='role',
            options={'ordering': ['community']},
        ),
    ]
