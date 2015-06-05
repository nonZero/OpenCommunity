# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from communities.models import Committee

from django.db import models, migrations


def community_to_committee(apps, schema_editor):
    Meeting = apps.get_model("meetings", "Meeting")
    meetings = Meeting.objects.all()
    for m in meetings:
        m.committee_id = m.community_id
        m.save()


class Migration(migrations.Migration):

    dependencies = [
        ('meetings', '0003_meeting_committee'),
    ]

    operations = [
        migrations.RunPython(community_to_committee),
    ]
