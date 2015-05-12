# coding: utf-8
from communities.models import Community
from django.core import serializers
from django.core.management.base import BaseCommand
from issues.models import Issue, IssueComment, IssueCommentRevision, Proposal
from meetings.models import Meeting, AgendaItem, MeetingParticipant, \
    MeetingExternalParticipant
from users.models import Membership, Invitation
import json


class Command(BaseCommand):
    help = "Dumps a community by it's pk"

    def add_arguments(self, parser):
        parser.add_argument('cid', nargs='+', type=int)

    def handle(self, *args, **options):
        all_cids = options['cid']

        for cid in all_cids:
            sets = (
                [m.user for m in Membership.objects.filter(community_id=cid)],
                Community.objects.filter(pk=cid),
                Invitation.objects.filter(community_id=cid),
                Membership.objects.filter(community_id=cid),
                Meeting.objects.filter(community_id=cid),
                Issue.objects.filter(community_id=cid),
                IssueComment.objects.filter(issue__community_id=cid),
                IssueCommentRevision.objects.filter(comment__issue__community_id=cid),
                Proposal.objects.filter(issue__community_id=cid),
                AgendaItem.objects.filter(issue__community_id=cid),
                MeetingParticipant.objects.filter(meeting__community_id=cid),
                MeetingExternalParticipant.objects.filter(meeting__community_id=cid),
            )

            l = []
            for qs in sets:
                l += list(qs)

            j = json.loads(serializers.serialize("json", l, use_natural_foreign_keys=True, indent=4))
            for o in j:
                o['pk'] = None

            data = json.dumps(j, sort_keys=True, indent=4)
            with open('community_{0}.json'.format(cid), 'w') as outfile:
                json.dump(data, outfile)
            print data
