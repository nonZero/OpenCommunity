from django import template
# from django.shortcuts import get_object_or_404

from issues.models import ProposalVote

register = template.Library()

@register.filter
def voted_on(u, proposal_id):
    voted = ProposalVote.objects.filter(
                            proposal_id=proposal_id,
                            user_id=u.id).exists()
    return voted


