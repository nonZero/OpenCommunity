from communities import models
from communities.forms import EditUpcomingMeetingForm, \
    PublishUpcomingMeetingForm, UpcomingMeetingParticipantsForm, StartMeetingForm, \
    EditUpcomingMeetingSummaryForm
from communities.models import SendToOption
from django.conf import settings
from django.contrib import messages
from django.core.urlresolvers import reverse_lazy
from django.db.models.aggregates import Max
from django.http.response import HttpResponse, HttpResponseBadRequest
from django.utils.translation import ugettext_lazy as _
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView
from issues.models import IssueStatus
from ocd.base_views import ProtectedMixin, AjaxFormView
import datetime
import json


class CommunityList(ListView):
    model = models.Community

    def get_queryset(self):
        qs = super(CommunityList, self).get_queryset()
        if self.request.user.is_superuser:
            return qs
        return qs.filter(is_public=True)

    def get_context_data(self, **kwargs):
        d = super(CommunityList, self).get_context_data(**kwargs)
        d['version'] = settings.OPENCOMMUNITY_VERSION
        return d


class CommunityModelMixin(ProtectedMixin):

    model = models.Community

    @property
    def community(self):
        return self.get_object()


class UpcomingMeetingView(CommunityModelMixin, DetailView):

    # TODO show empty page to 'issues.viewopen_issue'
    # TODO: show draft only to those allowed to manage it.
    required_permission = 'communities.access_community'

    template_name = "communities/upcoming.html"

    required_permission_for_post = 'community.editagenda_community'

    def post(self, request, *args, **kwargs):

        """ add / removes an issue from upcoming meeting """

        if settings.DEBUG:
            import time
            time.sleep(0.3)

        if 'issue' in request.POST:

            issue = self.get_object().issues.get(id=int(request.POST.get('issue')))
            if issue.changed_in_current():
                return HttpResponseBadRequest("can't remove this issue")
            add_to_meeting = request.POST['set'] == "0"
            issue.status = IssueStatus.IN_UPCOMING_MEETING if add_to_meeting \
                            else IssueStatus.OPEN
            last = self.get_object().upcoming_issues().aggregate(
                                     last=Max('order_in_upcoming_meeting'))['last']
            issue.order_in_upcoming_meeting = (last or 0) + 1
            issue.save()

            return HttpResponse(json.dumps(int(add_to_meeting)),
                                content_type='application/json')

        if 'issues[]' in request.POST:
            issues = [int(x) for x in request.POST.getlist('issues[]')]
            qs = self.get_object().upcoming_issues()
            for i, iid in enumerate(issues):
                qs.filter(id=iid).update(order_in_upcoming_meeting=i)

            return HttpResponse(json.dumps(True),
                                content_type='application/json')

        return HttpResponseBadRequest("Oops, bad request")


class PublishUpcomingMeetingPreviewView(CommunityModelMixin, DetailView):

    required_permission = 'communities.viewupcoming_community'

    template_name = "emails/agenda.html"


class EditUpcomingMeetingView(AjaxFormView, CommunityModelMixin, UpdateView):

    reload_on_success = True

    required_permission = 'community.editupcoming_community'
    
    form_class = EditUpcomingMeetingForm
    template_name = "communities/upcoming_form.html"

    def get_form(self, form_class):
        form = super(EditUpcomingMeetingView, self).get_form(form_class)
        c = self.get_object()
        if not c.straw_voting_enabled:
            del form.fields['voting_ends_at']

        return form

class EditUpcomingMeetingParticipantsView(AjaxFormView, CommunityModelMixin, UpdateView):

    reload_on_success = True

    required_permission = 'community.editparticipants_community'

    form_class = UpcomingMeetingParticipantsForm
    template_name = "communities/participants_form.html"


class PublishUpcomingView(AjaxFormView, CommunityModelMixin, UpdateView):

    reload_on_success = True

    required_permission = 'community.editagenda_community'

    form_class = PublishUpcomingMeetingForm
    template_name = "communities/publish_upcoming.html"

    def get_form(self, form_class):
        form = super(PublishUpcomingView, self).get_form(form_class)
        c = self.get_object()
        if not c.upcoming_meeting_started:
            form.fields['send_to'].choices = SendToOption.publish_choices

        return form

    def form_valid(self, form):

        resp = super(PublishUpcomingView, self).form_valid(form)

        c = self.object

        # increment agenda if publishing agenda.
        if not c.upcoming_meeting_started and form.cleaned_data['send_to'] != SendToOption.ONLY_ME:
            if form.cleaned_data['send_to'] == SendToOption.ALL_MEMBERS:
                c.upcoming_meeting_is_published = True
            else:
                c.upcoming_meeting_is_published = False
            c.upcoming_meeting_published_at = datetime.datetime.now()
            c.upcoming_meeting_version += 1

            c.save()

        template = 'protocol_draft' if c.upcoming_meeting_started else 'agenda'

        total = c.send_mail(template, self.request.user, form.cleaned_data['send_to'])
        messages.info(self.request, _("Sending to %d users") % total)

        return resp


class StartMeetingView(CommunityModelMixin, UpdateView):

    reload_on_success = True

    required_permission = 'community.editupcoming_community'

    form_class = StartMeetingForm

    #template_name = "communities/start_meeting.html"


class EditUpcomingSummaryView(AjaxFormView, CommunityModelMixin, UpdateView):

    reload_on_success = True

    required_permission = 'community.editupcoming_community'

    form_class = EditUpcomingMeetingSummaryForm

    template_name = "communities/edit_summary.html"


class ProtocolDraftPreviewView(CommunityModelMixin, DetailView):

    required_permission = 'meetings.add_meeting'

    template_name = "emails/protocol_draft.html"

    
def sum_votes(request, pk):
    if not request.user.is_superuser:
        return HttpResponse('--')
        
    c = models.Community.objects.get(pk=pk)
    c.sum_vote_results(only_when_over=False)
    return HttpResponse('-')
