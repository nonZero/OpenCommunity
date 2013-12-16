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
import json


last_vote = [7, 5, 19, 1]

def save_vote(request):
    if request.POST:
        issues_votes = json.loads(request.POST.get('vote'))
        if issues_votes:
            del last_vote[:]
            for v in issues_votes:
                last_vote.append(v[0])

            return HttpResponse(json_response('ok'))




def get_vote():
    return last_vote



