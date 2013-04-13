from django.http.response import HttpResponse
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from issues.views import CommunityMixin
from meetings import models
from meetings.forms import CreateMeetingForm
import json


class MeetingMixin(CommunityMixin):
    def get_queryset(self):
        return models.Meeting.objects.filter(community=self.community)

    def get_context_data(self, **kwargs):
        context = super(MeetingMixin, self).get_context_data(**kwargs)

        context['community'] = self.community

        return context


class MeetingCreateView(MeetingMixin, CreateView):
    model = models.Meeting
    form_class = CreateMeetingForm

    def form_valid(self, form):
        form.instance.community = self.community
        form.instance.created_by = self.request.user
        return super(MeetingCreateView, self).form_valid(form)


class MeetingDetailView(MeetingMixin, DetailView):
    model = models.Meeting

    def get_issues_queryset(self):
        return self.community.issues.filter(is_closed=False)

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
