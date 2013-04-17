from communities.models import Community
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404
from django.views.generic import ListView
from django.views.generic.base import View
from django.views.generic.detail import DetailView, SingleObjectMixin
from django.views.generic.edit import CreateView, UpdateView
from issues import models
from issues.forms import CreateIssueForm, CreateProposalForm, EditProposalForm
import datetime
import json


class CommunityMixin(object):

    @property
    def community(self):
        return get_object_or_404(Community, pk=self.kwargs['community_id'])


class IssueMixin(CommunityMixin):

    model = models.Issue

    def get_queryset(self):
        return models.Issue.objects.filter(community=self.community)

    def get_context_data(self, **kwargs):
        context = super(IssueMixin, self).get_context_data(**kwargs)

        context['community'] = self.community

        return context


class IssueList(IssueMixin, ListView):
    pass


class IssueDetailView(IssueMixin, DetailView):
    pass


class IssueCreateView(IssueMixin, CreateView):
    form_class = CreateIssueForm

    def form_valid(self, form):
        form.instance.community = self.community
        form.instance.created_by = self.request.user
        return super(IssueCreateView, self).form_valid(form)


class IssueEditView(IssueMixin, UpdateView):
    form_class = CreateIssueForm


class ProposalCreateView(IssueMixin, CreateView):

    model = models.Proposal
    form_class = CreateProposalForm

    @property
    def issue(self):
        return get_object_or_404(models.Issue, community=self.community, pk=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super(ProposalCreateView, self).get_context_data(**kwargs)

        context['issue'] = self.issue

        return context

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.issue = self.issue
        return super(ProposalCreateView, self).form_valid(form)

    def get_success_url(self):
        return self.issue.get_absolute_url()


class ProposalMixin(IssueMixin):
    model = models.Proposal

    @property
    def issue(self):
        return get_object_or_404(models.Issue, community=self.community,
                                 pk=self.kwargs['issue_id'])

    def get_queryset(self):
        return models.Proposal.objects.filter(issue=self.issue)


class ProposalDetailView(ProposalMixin, DetailView):

    def post(self, request, *args, **kwargs):

        # TODO AUTH

        p = self.get_object()
        p.is_accepted = request.POST['accepted'] == "0"
        p.accepted_at = datetime.datetime.now() if p.is_accepted else None
        p.save()

        return HttpResponse(json.dumps(int(p.is_accepted)),
                             content_type='application/json')


class ProposalEditView(ProposalMixin, UpdateView):
    form_class = EditProposalForm
