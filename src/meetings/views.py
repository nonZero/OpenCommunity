from django.contrib import messages
from django.db import transaction
from django.http.response import HttpResponse
from django.utils import timezone
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from issues.views import CommunityMixin
from meetings import models
from meetings.forms import CloseMeetingForm
from meetings.models import AgendaItem, MeetingParticipant
from ocd.base_views import AjaxFormView
from users.models import Membership
import datetime
from django.utils.translation import ugettext_lazy as _


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


class MeetingProtocolView(MeetingMixin, DetailView):
    required_permission = 'meetings.view_meeting'
    template_name = "emails/protocol.html"


class MeetingCreateView(AjaxFormView, MeetingMixin, CreateView):

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

            m = form.instance
            m.community = c
            m.created_by = self.request.user
            m.title = c.upcoming_meeting_title
            m.scheduled_at = (c.upcoming_meeting_scheduled_at
                                or datetime.datetime.now())
            m.location = c.upcoming_meeting_location
            m.comments = c.upcoming_meeting_comments
            m.guests = c.upcoming_meeting_guests

            m.save()

            c.upcoming_meeting_started = False
            c.upcoming_meeting_title = None
            c.upcoming_meeting_scheduled_at = None
            c.upcoming_meeting_location = None
            c.upcoming_meeting_comments = None
            c.upcoming_meeting_version = 0
            c.upcoming_meeting_is_published = False
            c.upcoming_meeting_published_at = None
            c.upcoming_meeting_guests = None
            c.save()

            for i, issue in enumerate(c.upcoming_issues()):

                AgendaItem.objects.create(meeting=m, issue=issue, order=i,
                                          closed=issue.completed)

                if issue.completed:
                    issue.is_closed = True
                    issue.closed_at_meeting = m
                    issue.in_upcoming_meeting = False
                    issue.order_in_upcoming_meeting = None
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

        total = c.send_mail('protocol', self.request.user,
                            form.cleaned_data['send_to'], {'object': m})
        messages.info(self.request, _("Sending to %d users") % total)

        return HttpResponse(m.get_absolute_url())
