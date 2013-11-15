from communities.models import Community
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.shortcuts import get_object_or_404

from issues.models import Issue, IssueComment, IssueCommentRevision, \
        Proposal, ProposalVote
from meetings.models import Meeting, AgendaItem, MeetingParticipant, \
    MeetingExternalParticipant
from users.models import Membership, Invitation
import json
from datetime import datetime


class Command(BaseCommand):
    help = "reset"

    def handle(self, *args, **options):
        cid = int(args[0])
        community = get_object_or_404(Community, pk=cid)
      
        un_summed_proposals = Proposal.objects.filter(
                        votes_pro__isnull=False)
        if un_summed_proposals.count() == 0:
            return

        member_count = community.get_members().count()
        for prop in un_summed_proposals:
            prop.votes_pro = None
            prop.votes_con = None
            prop.community_members = None
            prop.save()
