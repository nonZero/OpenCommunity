# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('communities', '0007_auto_20150514_1457'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='committee',
            unique_together=set([('community', 'slug')]),
        ),
    ]
