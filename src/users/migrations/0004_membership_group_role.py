# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('communities', '0010_auto_20150607_1148'),
        ('users', '0003_auto_20150607_1606'),
    ]

    operations = [
        migrations.AddField(
            model_name='membership',
            name='group_role',
            field=models.ForeignKey(related_name='memberships', verbose_name='Group', blank=True, to='communities.CommunityGroupRole', null=True),
        ),
    ]
