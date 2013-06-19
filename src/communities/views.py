from communities import models
from communities.forms import EditUpcomingMeetingForm, \
    PublishUpcomingMeetingForm, UpcomingMeetingParticipantsForm
from django.conf import settings
from django.core.urlresolvers import reverse
from django.http.response import HttpResponse
from django.shortcuts import redirect
from django.views.generic import ListView
from django.views.generic.base import RedirectView
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


class CommunityDetailView(CommunityModelMixin, SingleObjectMixin, RedirectView):

    def get_redirect_url(self, **kwargs):

        perm = 'issues.viewopen_issue'
        view_name = 'issues' if self.request.user.has_community_perm(
                                     self.community, perm) else 'history'

        return reverse(view_name, args=(str(self.community.id),))


class UpcomingMeetingView(CommunityModelMixin, DetailView):

    required_permission = 'communities.viewupcoming_community'

    template_name = "communities/upcoming.html"

    def get_issues_queryset(self, **kwargs):
        return self.get_object().issues.filter(is_closed=False, **kwargs)

    required_permission_for_post = 'community.editagenda_community'

    def post(self, request, *args, **kwargs):

        if settings.DEBUG:
            import time
            time.sleep(0.3)

        issue = self.get_issues_queryset().get(id=int(request.POST.get('issue')))

        add_to_meeting = request.POST['set'] == "0"
        issue.in_upcoming_meeting = add_to_meeting
        issue.save()

        return HttpResponse(json.dumps(int(add_to_meeting)),
                            content_type='application/json')


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
        c.upcoming_meeting_is_published = True
        c.upcoming_meeting_published_at = datetime.datetime.now()
        c.upcoming_meeting_version += 1

        c.save()

        return resp


class OngoingMeetingView(CommunityModelMixin, DetailView):

    required_permission = 'community.editupcoming_community'

    template_name = "communities/ongoing.html"

    def get_issues_queryset(self, **kwargs):
        return self.get_object().issues.filter(is_closed=False, **kwargs)

