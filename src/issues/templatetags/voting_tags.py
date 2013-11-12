from django import template
# from django.shortcuts import get_object_or_404

from issues.models import Proposal, Issue, ProposalVote

register = template.Library()

@register.filter
def voted_on(u, proposal_id):
    voted = ProposalVote.objects.filter(
                            proposal_id=proposal_id,
                            user_id=u.id).exists()
    return voted


@register.simple_tag(takes_context=True)
def user_votes_on_issue(context):
    issue = context['i']
    user_id = context['user'].id
    proposals = Proposal.objects.active().filter(issue_id=issue.id)
    votes_cnt = ProposalVote.objects.filter(
        proposal__in=proposals,
        user_id=user_id).count()
    return "{0}/{1}".format(votes_cnt, proposals.count())

