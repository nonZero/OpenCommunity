# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from acl.models import Role
from communities.models import Community, CommunityGroup, Committee, CommunityGroupRole
from django.db import models, migrations


def create_default_groups(apps, schema_editor):
    Membership = apps.get_model("users", "Membership")
    communities = Community.objects.all()
    committees = Committee.objects.all()

    for c in communities:
        # Creating groups to existing communities, similar to what they have before.
        CommunityGroup.objects.bulk_create([
            CommunityGroup(community=c, title='chairman', _order=0),
            CommunityGroup(community=c, title='board', _order=1),
            CommunityGroup(community=c, title='member', _order=2)
        ])
        # Creating roles for existing communities, similar to what they have before.
        Role.objects.bulk_create([
            Role(community=c, title='chairman', based_on='manager'),
            Role(community=c, title='board', based_on='participant'),
            Role(community=c, title='member', based_on='observer')
        ])
        # Assigning new group field values (FK).
        for member in c.memberships.all():
            member.group_name = c.groups.get(title=member.default_group_name)
            member.save()

    for c in committees:
        # Creating community group roles.
        CommunityGroupRole.objects.bulk_create([
            CommunityGroupRole(committee=c, role=c.community.roles.get(title="chairman"),
                               group=c.community.groups.get(title="chairman")),
            CommunityGroupRole(committee=c, role=c.community.roles.get(title="board"),
                               group=c.community.groups.get(title="board")),
            CommunityGroupRole(committee=c, role=c.community.roles.get(title="member"),
                               group=c.community.groups.get(title="member"))
        ])


class Migration(migrations.Migration):
    dependencies = [
        ('users', '0002_auto_20150607_1350'),
    ]

    operations = [
        migrations.RunPython(create_default_groups),
    ]
