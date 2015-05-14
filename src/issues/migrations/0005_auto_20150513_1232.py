# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from communities.models import Committee

from django.db import models, migrations
from issues.models import Issue


def community_to_committee(apps, schema_editor):
    # Issue = apps.get_model("issues", "Issue")
    issues = Issue.objects.all()
    for i in issues:
        i.committee = Committee.objects.get(pk=i.community.id)
        i.save()


class Migration(migrations.Migration):

    dependencies = [
        ('issues', '0004_issue_committee'),
    ]

    operations = [
        migrations.RunPython(community_to_committee),
    ]
