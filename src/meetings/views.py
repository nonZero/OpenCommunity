from django.contrib import messages
from django.db import transaction
from django.shortcuts import redirect
from django.utils import timezone
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, ModelFormMixin
from django.views.generic.list import ListView
from issues.views import CommunityMixin
from meetings import models
from meetings.forms import CloseMeetingForm
from meetings.models import AgendaItem
import datetime


class MeetingMixin(CommunityMixin):

    model = models.Meeting

    def get_queryset(self):
        return models.Meeting.objects.filter(community=self.community)

    def get_issues_queryset(self, **kwargs):
        return self.community.issues.filter(is_closed=False, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(MeetingMixin, self).get_context_data(**kwargs)

        context['community'] = self.community
        return context


class MeetingList(MeetingMixin, ListView):
    pass


class MeetingDetailView(MeetingMixin, DetailView):

    def get_context_data(self, **kwargs):
        context = super(MeetingDetailView, self).get_context_data(**kwargs)
        print self.get_issues_queryset()
        context['issues'] = self.get_issues_queryset()

        return context


class MeetingCreateView(MeetingMixin, CreateView):
    template_name = "meetings/meeting_close.html"
    form_class = CloseMeetingForm

    def get_initial(self):
        d = super(MeetingCreateView, self).get_initial()
        dt = self.community.upcoming_meeting_scheduled_at
        if not dt or dt > timezone.now():
            dt = timezone.now()
        d["held_at"] = dt
        return d

    def form_valid(self, form):

        with transaction.commit_on_success():
            c = self.community
            issues = c.issues_ready_to_close().filter(is_closed=False)
            if len(issues) == 0:
                messages.warning(self.request,
                                 _("Cannot close a meeting with no issues"))
                return redirect(c.get_upcoming_absolute_url())

            m = form.instance
            m.community = c
            m.created_by = self.request.user
            m.scheduled_at = (c.upcoming_meeting_scheduled_at
                                or datetime.datetime.now())
            m.location = c.upcoming_meeting_location
            m.comments = c.upcoming_meeting_comments

            m.save()

            c.upcoming_meeting_scheduled_at = None
            c.upcoming_meeting_location = None
            c.upcoming_meeting_comments = None
            c.upcoming_meeting_version = 0
            c.upcoming_meeting_is_published = False
            c.upcoming_meeting_published_at = None
            c.save()

            for i, issue in enumerate(issues):

                AgendaItem.objects.create(meeting=m, issue=issue, order=i)

                if len(issue.proposals.filter(active=True, is_accepted=True)):
                    issue.is_closed = True
                    issue.closed_at_meeting = m
                    issue.in_upcoming_meeting = False  # ???
                issue.save()

        return redirect(m.get_absolute_url())


