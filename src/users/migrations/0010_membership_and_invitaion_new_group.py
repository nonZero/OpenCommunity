# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from communities.models import CommunityGroup

from django.db import models, migrations


def create_group_name(apps, schema_editor):
    Membership = apps.get_model("users", "Membership")
    Invitation = apps.get_model("users", "Invitation")

    for member in Membership.objects.all():
        member.group_name = member.community.groups.get(title=member.default_group_name)
        member.save()

    for inv in Invitation.objects.all():
        inv.group_name = inv.community.groups.get(title=inv.default_group_name)
        inv.save()


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_auto_20150617_2139'),
    ]

    operations = [
        migrations.RunPython(create_group_name),
    ]
