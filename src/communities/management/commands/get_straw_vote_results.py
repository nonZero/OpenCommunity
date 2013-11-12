from communities.models import Community
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.shortcuts import get_object_or_404

from issues.models import Issue, IssueStatus, IssueComment, \
    IssueCommentRevision, Proposal, ProposalVote
from meetings.models import Meeting, AgendaItem, MeetingParticipant, \
    MeetingExternalParticipant
from users.models import Membership, Invitation
import json
from datetime import datetime


class Command(BaseCommand):
    help = "gather results after straw voting ends"

    def handle(self, *args, **options):
        cid = int(args[0])
        community = get_object_or_404(Community, pk=cid)
        community.sum_vote_results()
        
