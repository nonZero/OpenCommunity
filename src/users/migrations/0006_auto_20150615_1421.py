# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('communities', '0010_auto_20150607_1148'),
        ('users', '0005_auto_20150607_2221'),
    ]

    operations = [
        migrations.AddField(
            model_name='invitation',
            name='group_role',
            field=models.ForeignKey(related_name='invitations', verbose_name='Group', blank=True, to='communities.CommunityGroupRole', null=True),
        ),
        migrations.AlterUniqueTogether(
            name='invitation',
            unique_together=set([('group_role', 'email')]),
        ),
    ]
