# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('acl', '0001_initial'),
        ('communities', '0009_auto_20150603_1359'),
    ]

    operations = [
        migrations.CreateModel(
            name='CommunityGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=200)),
                ('community', models.ForeignKey(related_name='groups', to='communities.Community')),
            ],
            options={
                'verbose_name': 'Group',
                'verbose_name_plural': 'Groups',
            },
        ),
        migrations.CreateModel(
            name='CommunityGroupRole',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('committee', models.ForeignKey(related_name='group_roles', to='communities.Committee')),
                ('group', models.ForeignKey(related_name='group_roles', to='communities.CommunityGroup')),
                ('role', models.ForeignKey(related_name='group_roles', to='acl.Role')),
            ],
            options={
                'verbose_name': 'Group Role',
                'verbose_name_plural': 'Group Roles',
            },
        ),
        migrations.AlterUniqueTogether(
            name='communitygrouprole',
            unique_together=set([('group', 'role', 'committee')]),
        ),
        migrations.AlterUniqueTogether(
            name='communitygroup',
            unique_together=set([('community', 'title')]),
        ),
        migrations.AlterOrderWithRespectTo(
            name='communitygroup',
            order_with_respect_to='community',
        ),
    ]
