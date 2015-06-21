# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def create_group_name(apps, schema_editor):
    Membership = apps.get_model("users", "Membership")

    for member in Membership.objects.all():
        if not member.group_name:
            member.group_name = member.community.groups.get(title=member.default_group_name)
            member.save()


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_membership_and_invitaion_new_group'),
    ]

    operations = [
        migrations.RunPython(create_group_name),
        migrations.AlterField(
            model_name='membership',
            name='group_name',
            field=models.ForeignKey(related_name='memberships', verbose_name='Group', to='communities.CommunityGroup'),
        ),
        migrations.AlterUniqueTogether(
            name='membership',
            unique_together=set([('community', 'user', 'group_name')]),
        ),
    ]
