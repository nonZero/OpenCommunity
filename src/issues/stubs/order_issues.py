from django.http.response import HttpResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, render, redirect
from django.template import RequestContext
from django.template.loader import render_to_string
from django.views.generic import ListView
from django.views.generic.base import View
from django.views.generic import UpdateView
from django.views.generic.detail import DetailView, SingleObjectMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import UpdateView
from ocd.base_views import CommunityMixin, AjaxFormView, json_response
from issues.models import Issue, IssueRankingVote
import json


last_vote = [5,19,1,7,23]

def process_vote_stub(current_order, prev_order):
    issues = Issue.objects.in_bulk(current_order)
    for ord, id in enumerate(current_order):
        if issues[id].order_by_votes != ord:
            issues[id].order_by_votes = ord
            issues[id].save()

def save_vote(request):
    if request.POST:
        current_vote = json.loads(request.POST.get('new_order'))
        prev_vote = IssueRankingVote.objects.filter(
                            voted_by=request.user,
                            issue__community_id=request.POST['community_id']) \
                            .order_by('rank')
        
        if current_vote:
            prev_vote_as_list = list(prev_vote.values_list('issue_id', flat=True))
            for v in prev_vote:
                v.delete()
            for i, v in enumerate(current_vote):
                IssueRankingVote.objects.create(
                    voted_by=request.user,
                    issue_id=v,
                    rank=i
                )
            print current_vote, prev_vote_as_list
            process_vote_stub(current_vote, prev_vote)
            return HttpResponse(json_response('ok'))



def get_sorted_issues(community_id):
    # votes = IssueRankingVote.objects.filter(issue__community_id=community_id)
    i_order = last_vote  # api: get_sorted_issues(community_id)
    # update issue's order ranking 
    return ''



