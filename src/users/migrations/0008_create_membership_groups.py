# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from communities.models import CommunityGroup, Community

from django.db import models, migrations


def create_default_groups(apps, schema_editor):
    Membership = apps.get_model("users", "Membership")
    communities = Community.objects.all()

    for c in communities:
        # Assigning new group field values (FK).
        for member in c.memberships.all():
            member.group_name = CommunityGroup.objects.get(community=c, title=member.default_group_name)
            member.save()


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_auto_20150615_1535'),
    ]

    operations = [
        migrations.RunPython(create_default_groups),
    ]
