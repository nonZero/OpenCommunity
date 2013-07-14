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

    def handle(self, *args, **options):
        cid = int(args[0])

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

        j = json.loads(serializers.serialize("json", l, use_natural_keys=True, indent=4))
        for o in j:
            o['pk'] = None

        print json.dumps(j, indent=4)
