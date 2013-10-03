from django.contrib import messages
from django.http.response import HttpResponse
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.views.generic.base import RedirectView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from issues.views import CommunityMixin
from meetings import models
from meetings.forms import CloseMeetingForm
from ocd.base_views import AjaxFormView


class MeetingMixin(CommunityMixin):

    model = models.Meeting

    def get_queryset(self):
        return models.Meeting.objects.filter(community=self.community)


class MeetingList(MeetingMixin, RedirectView):
    required_permission = 'meetings.view_meeting'

    def get_redirect_url(self, **kwargs):
        o = models.Meeting.objects.filter(community=self.community).latest('held_at')
        if o:
            return o.get_absolute_url()


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

        m = self.community.close_meeting(form.instance, self.request.user)

        total = self.community.send_mail('protocol', self.request.user,
                            form.cleaned_data['send_to'], {'object': m})

        messages.info(self.request, _("Sending to %d users") % total)

        return HttpResponse(m.get_absolute_url())
