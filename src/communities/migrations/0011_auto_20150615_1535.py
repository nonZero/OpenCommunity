# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('communities', '0010_auto_20150607_1148'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='communitygrouprole',
            options={'ordering': ['committee'], 'verbose_name': 'Group Role', 'verbose_name_plural': 'Group Roles'},
        ),
    ]
