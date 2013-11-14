from django import template
from issues.models import Proposal, ProposalVote


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
    proposals = Proposal.objects.open().filter(issue_id=issue.id)
    votes_cnt = ProposalVote.objects.filter(
        proposal__in=proposals,
        user_id=user_id).count()
    return "<span class='votes_count'>{0}</span>/<span class='proposal_count'>{1}</span>".format(votes_cnt, proposals.count())


@register.filter
def vote_percentage(proposal):
    if proposal.votes_pro is None:
        return 'undefined'
    votes = proposal.votes_pro + proposal.votes_con
    print votes ,proposal.community_members
    percentage = (float(votes) / float(proposal.community_members)) * 100.0  
    return str(percentage)


@register.filter    
def subtract(value, arg):
    if arg is None:
        return value
    return value - arg
