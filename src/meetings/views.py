from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from issues.views import CommunityMixin
from meetings import models


class MeetingMixin(CommunityMixin):
    def get_queryset(self):
        return models.Meeting.objects.filter(community=self.community)

    def get_issues_queryset(self, **kwargs):
        return self.community.issues.filter(is_closed=False, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(MeetingMixin, self).get_context_data(**kwargs)

        context['community'] = self.community

        return context


class MeetingList(MeetingMixin, ListView):
    model = models.Meeting


class MeetingDetailView(MeetingMixin, DetailView):
    model = models.Meeting

    def get_context_data(self, **kwargs):
        context = super(MeetingDetailView, self).get_context_data(**kwargs)
        print self.get_issues_queryset()
        context['issues'] = self.get_issues_queryset()

        return context


