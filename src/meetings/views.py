from django.http.response import HttpResponse, HttpResponseForbidden, \
    HttpResponseServerError
from django.shortcuts import redirect
from django.views.generic.base import View
from django.views.generic.detail import DetailView, SingleObjectMixin
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from issues.views import CommunityMixin
from meetings import models
from meetings.forms import CreateMeetingForm
from meetings.models import AgendaItem
import datetime
import json


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


class MeetingCreateView(MeetingMixin, CreateView):
    model = models.Meeting
    form_class = CreateMeetingForm

    def form_valid(self, form):
        form.instance.community = self.community
        form.instance.created_by = self.request.user
        return super(MeetingCreateView, self).form_valid(form)


class MeetingDetailView(MeetingMixin, DetailView):
    model = models.Meeting

    def get_context_data(self, **kwargs):
        context = super(MeetingDetailView, self).get_context_data(**kwargs)
        print self.get_issues_queryset()
        context['issues'] = self.get_issues_queryset()

        return context

    def post(self, request, *args, **kwargs):

        issue = self.get_issues_queryset().get(id=int(request.POST.get('issue')))

        add_to_meeting = request.POST['set'] == "0"
        issue.in_upcoming_meeting = add_to_meeting
        issue.save()

        return HttpResponse(json.dumps(int(add_to_meeting)), content_type='application/json')


class PublishMeetingView(MeetingMixin, SingleObjectMixin, View):
    model = models.Meeting

    def post(self, request, *args, **kwargs):

        # TODO AUTH

        m = self.get_object()
        m.is_published = True
        m.published_at = datetime.datetime.now()
        m.version += 1

        m.agenda_items.all().delete()
        for issue in self.get_issues_queryset(in_upcoming_meeting=True):
            AgendaItem.objects.create(meeting=m, issue=issue)

        m.save()

        return redirect(m.get_absolute_url())

        # return HttpResponse(json.dumps(int(add_to_meeting)), content_type='application/json')
