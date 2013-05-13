from communities import models
from communities.forms import EditUpcomingMeetingForm, \
    PublishUpcomingMeetingForm
from django.conf import settings
from django.core.urlresolvers import reverse
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView
from django.views.generic.base import RedirectView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView
from ocd.views import ProtectedMixin
import datetime
import json


class CommunityList(ListView):
    model = models.Community


class CommunityDetailView(RedirectView):

    def get_redirect_url(self, **kwargs):

        self.community = get_object_or_404(models.Community,
                                           pk=self.kwargs['pk'])

        return reverse('issues', args=(str(self.community.id),))


class UpcomingMeetingView(ProtectedMixin, DetailView):
    model = models.Community
    template_name = "communities/upcoming.html"

    def get_issues_queryset(self, **kwargs):
        return self.get_object().issues.filter(is_closed=False, **kwargs)

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


class EditUpcomingMeetingView(ProtectedMixin, UpdateView):
    model = models.Community
    form_class = EditUpcomingMeetingForm
    template_name = "communities/upcoming_form.html"

    def get_success_url(self):
        return self.get_object().get_upcoming_absolute_url()


class PublishUpcomingView(ProtectedMixin, UpdateView):
    model = models.Community
    form_class = PublishUpcomingMeetingForm
    template_name = "communities/publish_upcoming.html"

    def form_valid(self, form):

        resp = super(PublishUpcomingView, self).form_valid(form)

        c = self.object
        c.upcoming_meeting_is_published = True
        c.upcoming_meeting_published_at = datetime.datetime.now()
        c.upcoming_meeting_version += 1

        c.save()

        return redirect(c.get_upcoming_absolute_url())


class OngoingMeetingView(ProtectedMixin, DetailView):
    model = models.Community
    template_name = "communities/ongoing.html"

    def get_issues_queryset(self, **kwargs):
        return self.get_object().issues.filter(is_closed=False, **kwargs)

