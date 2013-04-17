from communities import models
from django.conf import settings
from django.core.urlresolvers import reverse
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404
from django.views.generic import ListView
from django.views.generic.base import RedirectView, View
from django.views.generic.detail import DetailView, SingleObjectMixin
from django.shortcuts import redirect
import datetime
import json


class CommunityList(ListView):
    model = models.Community


class CommunityDetailView(RedirectView):
    def get_redirect_url(self, **kwargs):

        self.community = get_object_or_404(models.Community, 
                                           pk=self.kwargs['pk'])

        return reverse('issues', args=(str(self.community.id),))


class UpcomingMeetingView(DetailView):
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
        print issue, add_to_meeting
        issue.in_upcoming_meeting = add_to_meeting
        issue.save()

        return HttpResponse(json.dumps(int(add_to_meeting)),
                            content_type='application/json')


class PublishMeetingView(SingleObjectMixin, View):
    model = models.Community

    def post(self, request, *args, **kwargs):

        # TODO AUTH
        c = self.get_object()
        c.upcoming_meeting_is_published = True
        c.upcoming_meeting_published_at = datetime.datetime.now()
        c.upcoming_meeting_version += 1

        c.save()

        return redirect(c.get_upcoming_absolute_url())
