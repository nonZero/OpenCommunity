# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


def create_groups(apps, schema_editor):
    Invitation = apps.get_model("users", "Invitation")

    for i in Invitation.objects.all():
        # Assigning groups field from group_name.
        i.groups.add(i.group_name)
        i.save()


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0013_auto_20151020_1048'),
    ]

    operations = [
        migrations.RunPython(create_groups),
    ]
