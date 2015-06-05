# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def copy_communities(apps, schema_editor):
    Community = apps.get_model("communities", "Community")
    Committee = apps.get_model("communities", "Committee")
    communities = Community.objects.all()
    for c in communities:
        committe = Committee.objects.create(pk=c.id, community=c)
        committe.name = c.name
        committe.is_public = c.is_public
        committe.logo = c.logo
        committe.official_identifier = c.official_identifier
        committe.upcoming_meeting_started = c.upcoming_meeting_started
        committe.upcoming_meeting_title = c.upcoming_meeting_title
        committe.upcoming_meeting_scheduled_at = c.upcoming_meeting_scheduled_at
        committe.upcoming_meeting_location = c.upcoming_meeting_location
        committe.upcoming_meeting_comments = c.upcoming_meeting_comments
        committe.upcoming_meeting_guests = c.upcoming_meeting_guests
        committe.upcoming_meeting_version = c.upcoming_meeting_version
        committe.upcoming_meeting_is_published = c.upcoming_meeting_is_published
        committe.upcoming_meeting_published_at = c.upcoming_meeting_published_at
        committe.upcoming_meeting_summary = c.upcoming_meeting_summary
        committe.board_name = c.board_name
        committe.straw_voting_enabled = c.straw_voting_enabled
        committe.issue_ranking_enabled = c.issue_ranking_enabled
        committe.voting_ends_at = c.voting_ends_at
        committe.referendum_started = c.referendum_started
        committe.referendum_started_at = c.referendum_started_at
        committe.referendum_ends_at = c.referendum_ends_at
        committe.default_quorum = c.default_quorum
        committe.allow_links_in_emails = c.allow_links_in_emails
        committe.email_invitees = c.email_invitees
        committe.register_missing_board_members = c.register_missing_board_members
        committe.inform_system_manager = c.inform_system_manager
        committe.no_meetings_community = c.no_meetings_community
        committe.slug = "main"

        for member in c.upcoming_meeting_participants.all():
            committe.upcoming_meeting_participants.add(member)

        committe.save()


class Migration(migrations.Migration):

    dependencies = [
        ('communities', '0003_committee'),
    ]

    operations = [
        migrations.RunPython(copy_communities),
    ]
