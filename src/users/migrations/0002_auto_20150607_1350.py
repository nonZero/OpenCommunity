# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('communities', '0010_auto_20150607_1148'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='membership',
            name='group_name',
            field=models.ForeignKey(related_name='memberships', verbose_name='Group', blank=True, to='communities.CommunityGroup', null=True),
        ),
        migrations.AlterField(
            model_name='membership',
            name='default_group_name',
            field=models.CharField(max_length=50, verbose_name='Old group', choices=[(b'member', 'member'), (b'board', 'board'), (b'secretary', 'secretary'), (b'chairman', 'chairman')]),
        ),
    ]
