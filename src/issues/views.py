from communities.models import Community
from django.shortcuts import get_object_or_404
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from issues import models
# from django.views.generic.base import RedirectView


class IssueMixin(object):

    def get_queryset(self):
        self.community = get_object_or_404(Community, pk=self.kwargs['community_id'])
        return models.Issue.objects.filter(community=self.community)

    def get_context_data(self, **kwargs):
        context = super(IssueMixin, self).get_context_data(**kwargs)

        context['community'] = self.community

        return context

class IssueList(IssueMixin, ListView):
    model = models.Issue


class IssueDetailView(IssueMixin, DetailView):
    model = models.Issue


# class CommunityDetailView(RedirectView):
#    model = models.Community
