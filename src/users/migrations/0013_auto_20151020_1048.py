# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('communities', '0011_auto_20150615_1535'),
        ('users', '0012_auto_20150621_1538'),
    ]

    operations = [
        migrations.AddField(
            model_name='invitation',
            name='groups',
            field=models.ManyToManyField(related_name='invitations', verbose_name='Groups', to='communities.CommunityGroup'),
        ),
        migrations.AlterField(
            model_name='invitation',
            name='group_name',
            field=models.ForeignKey(related_name='g_invitations', verbose_name='Group', blank=True, to='communities.CommunityGroup', null=True),
        ),
        migrations.AlterUniqueTogether(
            name='invitation',
            unique_together=set([('community', 'email')]),
        ),
    ]
