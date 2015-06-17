# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('communities', '0011_auto_20150615_1535'),
        ('users', '0008_create_membership_groups'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='membership',
            options={'ordering': ['community'], 'verbose_name': 'Community Member', 'verbose_name_plural': 'Community Members'},
        ),
        migrations.RemoveField(
            model_name='membership',
            name='group_role',
        ),
        migrations.AddField(
            model_name='invitation',
            name='group_name',
            field=models.ForeignKey(related_name='invitations', verbose_name='Group', blank=True, to='communities.CommunityGroup', null=True),
        ),
        migrations.AlterUniqueTogether(
            name='invitation',
            unique_together=set([('group_name', 'email')]),
        ),
    ]
