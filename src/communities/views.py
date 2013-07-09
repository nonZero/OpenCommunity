from communities import models
from communities.forms import EditUpcomingMeetingForm, \
    PublishUpcomingMeetingForm, UpcomingMeetingParticipantsForm, StartMeetingForm, \
    EditUpcomingMeetingSummaryForm
from communities.models import SendToOption
from django.conf import settings
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.db.models.aggregates import Max
from django.http.response import HttpResponse
from django.utils.translation import ugettext_lazy as _
from django.views.generic import ListView
from django.views.generic.base import RedirectView, View
from django.views.generic.detail import DetailView, SingleObjectMixin
from django.views.generic.edit import UpdateView
from ocd.base_views import ProtectedMixin, LoginRequiredMixin, AjaxFormView
import datetime
import json


class CommunityList(LoginRequiredMixin, ListView):
    model = models.Community

    def get_queryset(self):
        qs = super(CommunityList, self).get_queryset()
        if self.request.user.is_superuser:
            return qs
        return qs.filter(memberships__user=self.request.user)


class CommunityModelMixin(ProtectedMixin):

    model = models.Community

    @property
    def community(self):
        return self.get_object()


class UpcomingMeetingView(CommunityModelMixin, DetailView):

    # TODO show empty page to 'issues.viewopen_issue'
    # TODO: show draft only to those allowed to manage it.
    required_permission = 'communities.viewupcoming_community'

    template_name = "communities/upcoming.html"

    def get_issues_queryset(self, **kwargs):
        return self.get_object().issues.filter(is_closed=False, **kwargs)

    required_permission_for_post = 'community.editagenda_community'

    def post(self, request, *args, **kwargs):

        """ add / removes an issue from upcoming meeting """

        if settings.DEBUG:
            import time
            time.sleep(0.3)

        issue = self.get_issues_queryset().get(id=int(request.POST.get('issue')))

        add_to_meeting = request.POST['set'] == "0"
        issue.in_upcoming_meeting = add_to_meeting
        last = self.get_object().upcoming_issues().aggregate(
                                 last=Max('order_in_upcoming_meeting'))['last']
        issue.order_in_upcoming_meeting = (last or 0) + 1
        issue.save()

        return HttpResponse(json.dumps(int(add_to_meeting)),
                            content_type='application/json')


class PublishUpcomingMeetingPreviewView(CommunityModelMixin, DetailView):

    required_permission = 'communities.viewupcoming_community'

    template_name = "emails/agenda.html"

    def get_issues_queryset(self, **kwargs):
        return self.get_object().issues.filter(is_closed=False, **kwargs)


class EditUpcomingMeetingView(AjaxFormView, CommunityModelMixin, UpdateView):

    reload_on_success = True

    required_permission = 'communities.editupcoming_community'

    form_class = EditUpcomingMeetingForm
    template_name = "communities/upcoming_form.html"


class EditUpcomingMeetingParticipantsView(AjaxFormView, CommunityModelMixin, UpdateView):

    reload_on_success = True

    required_permission = 'communities.editparticipants_community'

    form_class = UpcomingMeetingParticipantsForm
    template_name = "communities/participants_form.html"


class PublishUpcomingView(AjaxFormView, CommunityModelMixin, UpdateView):

    reload_on_success = True

    required_permission = 'community.editagenda_community'

    form_class = PublishUpcomingMeetingForm
    template_name = "communities/publish_upcoming.html"

    def form_valid(self, form):

        resp = super(PublishUpcomingView, self).form_valid(form)

        c = self.object

        # increment agenda if publishing agenda.
        if not c.upcoming_meeting_started and form.cleaned_data['send_to'] != SendToOption.ONLY_ME:
            c.upcoming_meeting_is_published = True
            c.upcoming_meeting_published_at = datetime.datetime.now()
            c.upcoming_meeting_version += 1

            c.save()

        template = 'protocol_draft' if c.upcoming_meeting_started else 'agenda'

        total = c.send_mail(template, self.request.user, form.cleaned_data['send_to'])
        messages.info(self.request, _("Sending to %d users") % total)

        return resp


class StartMeetingView(AjaxFormView, CommunityModelMixin, UpdateView):

    reload_on_success = True

    required_permission = 'community.editupcoming_community'

    form_class = StartMeetingForm

    template_name = "communities/start_meeting.html"


class EditUpcomingSummaryView(AjaxFormView, CommunityModelMixin, UpdateView):

    reload_on_success = True

    required_permission = 'community.editupcoming_community'

    form_class = EditUpcomingMeetingSummaryForm

    template_name = "communities/edit_summary.html"


class ProtocolDraftPreviewView(CommunityModelMixin, DetailView):

    required_permission = 'meetings.add_meeting'

    template_name = "emails/protocol_draft.html"
