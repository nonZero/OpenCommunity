from communities.models import Community
from django.conf import settings
from django.db import models
from django.utils.formats import date_format, time_format
from issues.models import Issue
from django.utils.translation import ugettext, ugettext_lazy as _


class AgendaItem(models.Model):
    meeting = models.ForeignKey('Meeting', verbose_name=_("Meeting"))
    issue = models.ForeignKey(Issue, verbose_name=_("Issue"))
    order = models.PositiveIntegerField(default=100, verbose_name=_("Order"))

    def __unicode__(self):
        return self.issue.title

    class Meta:
        unique_together = (("meeting", "issue"),)
        verbose_name = _("Agenda Item")
        verbose_name_plural = _("Agenda Items")


class Meeting(models.Model):
    community = models.ForeignKey(Community, related_name="meetings", verbose_name=_("Community"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created at"))
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="meetings_created", verbose_name=_("Created by"))

    scheduled_at = models.DateTimeField(verbose_name=_("Scheduled at"))
    location = models.CharField(max_length=300, null=True, blank=True, verbose_name=_("Location"))
    comments = models.TextField(null=True, blank=True, verbose_name=_("Comments"))

    agenda_items = models.ManyToManyField(Issue, through=AgendaItem, blank=True, verbose_name=_("Agenda items"))

    participants = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                          related_name="participated_in_meeting", verbose_name=_("Participants"))

    is_published = models.BooleanField(_("Is published"), default=False)
    published_at = models.DateTimeField(_("Published at"), blank=True, null=True)
    version = models.IntegerField(_("Version"), default=0)

    is_closed = models.BooleanField(default=False, verbose_name=_("Is closed"))
    closed_at = models.DateTimeField(_("Closed at"), blank=True, null=True)
    closed_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="meetings_closed",
                                  null=True, blank=True, verbose_name=_("Closed by"))

    class Meta:
        verbose_name = _("Meeting")
        verbose_name_plural = _("Meetings")

    def __unicode__(self):
        return date_format(self.scheduled_at) + ", " + time_format(self.scheduled_at)

    @models.permalink
    def get_absolute_url(self):
        return ("meeting", (str(self.community.pk), str(self.pk),))


class MeetingExternalParticipant(models.Model):
    meeting = models.ForeignKey(Meeting, verbose_name=_("Meeting"))
    name = models.CharField(max_length=200, verbose_name=_("Name"))

    class Meta:
        verbose_name = _("Meeting External Participant")
        verbose_name_plural = _("Meeting External Participants")

    def __unicode__(self):
        return self.name
