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
from meetings.models import AgendaItem, MeetingParticipant
from users.models import Membership
import datetime


class MeetingMixin(CommunityMixin):

    model = models.Meeting

    def get_queryset(self):
        return models.Meeting.objects.filter(community=self.community)


class MeetingList(MeetingMixin, ListView):
    required_permission = 'meetings.view_meeting'


class MeetingDetailView(MeetingMixin, DetailView):
    required_permission = 'meetings.view_meeting'

    def get_context_data(self, **kwargs):
        d = super(MeetingDetailView, self).get_context_data(**kwargs)
        o = self.get_object()
        d['guest_list'] = o.get_guest_list()
        d['total_participants'] = len(d['guest_list']) + o.participants.count()
        return d


class MeetingCreateView(MeetingMixin, CreateView):

    required_permission = 'meetings.add_meeting'

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
            m.guests = c.upcoming_meeting_guests

            m.save()

            c.upcoming_meeting_scheduled_at = None
            c.upcoming_meeting_location = None
            c.upcoming_meeting_comments = None
            c.upcoming_meeting_version = 0
            c.upcoming_meeting_is_published = False
            c.upcoming_meeting_published_at = None
            c.upcoming_meeting_guests = None
            c.save()

            for i, issue in enumerate(issues):

                AgendaItem.objects.create(meeting=m, issue=issue, order=i)

                if len(issue.proposals.filter(active=True, is_accepted=True)):
                    issue.is_closed = True
                    issue.closed_at_meeting = m
                    issue.in_upcoming_meeting = False  # ???
                issue.save()

            for i, p in enumerate(c.upcoming_meeting_participants.all()):

                try:
                    mm = p.memberships.get(community=c)
                except Membership.DoesNotExist:
                    mm = None

                MeetingParticipant.objects.create(meeting=m, ordinal=i, user=p,
                      display_name=p.display_name,
                      default_group_name=mm.default_group_name if mm else None)

            c.upcoming_meeting_participants = []

        return redirect(m.get_absolute_url())
