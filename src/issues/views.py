from communities.models import Community
from django.shortcuts import get_object_or_404
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from issues import models
from issues.forms import CreateIssueForm, CreateProposalForm
# from django.views.generic.base import RedirectView


class CommunityMixin(object):

    @property
    def community(self):
        return get_object_or_404(Community, pk=self.kwargs['community_id'])


class IssueMixin(CommunityMixin):
    def get_queryset(self):
        return models.Issue.objects.filter(community=self.community)

    def get_context_data(self, **kwargs):
        context = super(IssueMixin, self).get_context_data(**kwargs)

        context['community'] = self.community

        return context


class IssueList(IssueMixin, ListView):
    model = models.Issue


class IssueDetailView(IssueMixin, DetailView):
    model = models.Issue


class IssueCreateView(IssueMixin, CreateView):

    model = models.Issue
    form_class = CreateIssueForm

    def form_valid(self, form):
        form.instance.community = self.community
        form.instance.created_by = self.request.user
        return super(IssueCreateView, self).form_valid(form)


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


class ProposalDetailView(IssueMixin, DetailView):

    model = models.Proposal

    @property
    def issue(self):
        return get_object_or_404(models.Issue, community=self.community,
                                 pk=self.kwargs['issue_id'])

    def get_queryset(self):
        return models.Proposal.objects.filter(issue=self.issue)

    def get_context_data(self, **kwargs):
        context = super(ProposalDetailView, self).get_context_data(**kwargs)

        context['issue'] = self.issue

        return context
