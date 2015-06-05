# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from communities.legacy_mapping import TITLE_TO_SLUG

from django.db import models, migrations


def create_community_slug(apps, schema_editor):
    Community = apps.get_model("communities", "Community")
    communities = Community.objects.filter(slug__isnull=True)
    for c in communities:
        c.slug = TITLE_TO_SLUG.get(c.name, "c{}".format(c.id))
        c.save()


class Migration(migrations.Migration):

    dependencies = [
        ('communities', '0008_auto_20150514_1518'),
    ]

    operations = [
        migrations.RunPython(create_community_slug),
    ]
