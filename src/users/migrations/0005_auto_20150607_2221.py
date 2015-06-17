# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def create_group_roles(apps, schema_editor):
    Membership = apps.get_model("users", "Membership")
    members = Membership.objects.all()
    # for m in members:
    #     m.group_role = m.group_name.group_roles.get(committee__community=m.community)
    #     m.save()


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_membership_group_role'),
    ]

    operations = [
        migrations.RunPython(create_group_roles),
    ]
