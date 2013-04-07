from communities.models import Community
from django.conf import settings
from django.db import models
from django.utils.formats import date_format, time_format
from issues.models import Issue


class AgendaItem(models.Model):
    meeting = models.ForeignKey('Meeting')
    issue = models.ForeignKey(Issue)
    order = models.PositiveIntegerField(default=100)
    resolved = models.BooleanField(default=False)

    def __unicode__(self):
        return self.issue.title

    class Meta:
        unique_together = (("meeting", "issue"),)


class Meeting(models.Model):
    community = models.ForeignKey(Community, related_name="meetings")
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="meetings_created")

    scheduled_at = models.DateTimeField()
    location = models.CharField(max_length=300, null=True, blank=True)
    comments = models.TextField(null=True, blank=True)

    agenda_items = models.ManyToManyField(Issue, through=AgendaItem, blank=True)

    participants = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                          related_name="participated_in_meeting")

    is_closed = models.BooleanField(default=False)
    closed_at = models.DateTimeField(auto_now_add=True)
    closed_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="meetings_closed",
                                  null=True, blank=True)

    def __unicode__(self):
        return date_format(self.scheduled_at) + ", " + time_format(self.scheduled_at)


class MeetingExternalParticipant(models.Model):
    meeting = models.ForeignKey(Meeting)
    name = models.CharField(max_length=200)

    def __unicode__(self):
        return self.name
