from communities.models import Community
from django.conf import settings
from django.db import models
from django.utils.formats import date_format, time_format
from django.utils.translation import ugettext_lazy as _
from issues.models import Issue
from users.default_roles import DefaultGroups
from ocd.base_models import UIDMixin


class AgendaItem(models.Model):
    meeting = models.ForeignKey('Meeting', verbose_name=_("Meeting"),
                                related_name="agenda")
    issue = models.ForeignKey(Issue, verbose_name=_("Issue"))
    order = models.PositiveIntegerField(default=100, verbose_name=_("Order"))
    closed = models.BooleanField(_('Closed'), default=True)

    class Meta:
        unique_together = (("meeting", "issue"),)
        verbose_name = _("Agenda Item")
        verbose_name_plural = _("Agenda Items")

    def __unicode__(self):
        return self.issue.title

#     def natural_key(self):
#         return (self.meeting.natural_key(), self.issue.natural_key())
#     natural_key.dependencies = ['meetings.meeting', 'issues.issue']


class Meeting(UIDMixin):
    community = models.ForeignKey(Community, related_name="meetings", verbose_name=_("Community"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created at"))
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="meetings_created", verbose_name=_("Created by"))

    held_at = models.DateTimeField(_("Held at"))

    title = models.CharField(_("Title"), max_length=300, null=True, blank=True)
    scheduled_at = models.DateTimeField(_("Scheduled at"),
                                        null=True, blank=True)
    location = models.CharField(_("Location"), max_length=300, null=True, blank=True)
    comments = models.TextField(_("Comments"), null=True, blank=True)

    summary = models.TextField(_("Summary"), null=True, blank=True)

    agenda_items = models.ManyToManyField(Issue, through=AgendaItem, blank=True, verbose_name=_("Agenda items"))

    participants = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                          related_name="participated_in_meeting",
                                          verbose_name=_("Participants"),
                                          through='MeetingParticipant')

    guests = models.TextField(_("Guests"), null=True, blank=True,
                           help_text=_("Enter each guest in a separate line"))

    class Meta:
        verbose_name = _("Meeting")
        verbose_name_plural = _("Meetings")
        ordering = ("-held_at", )

    def __unicode__(self):
        return date_format(self.scheduled_at) + ", " + time_format(self.scheduled_at)

    def get_guest_list(self):
        if not self.guests:
            return []
        return filter(None, [s.strip() for s in self.guests.splitlines()])

    @models.permalink
    def get_absolute_url(self):
        return ("meeting", (str(self.community.pk), str(self.pk),))


class MeetingParticipant(models.Model):
    meeting = models.ForeignKey(Meeting, verbose_name=_("Meeting"), 
                                related_name="participations")
    ordinal = models.PositiveIntegerField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             related_name="participations")
    # denormalize for history :
    display_name = models.CharField(_("Name"), max_length=200)
    default_group_name = models.CharField(_('Group'), max_length=50,
                                          choices=DefaultGroups.CHOICES,
                                          null=True, blank=True)

    class Meta:
        verbose_name = _("Meeting Participant")
        verbose_name_plural = _("Meeting Participants")
        unique_together = (('meeting', 'ordinal'), ('meeting', 'user'))

    def __unicode__(self):
        return self.user

#     def natural_key(self):
#         return (self.meeting.natural_key(), self.user.natural_key())
#     natural_key.dependencies = ['meetings.meeting', 'users.ocuser']


class MeetingExternalParticipant(models.Model):
    meeting = models.ForeignKey(Meeting, verbose_name=_("Meeting"))
    name = models.CharField(max_length=200, verbose_name=_("Name"))

    class Meta:
        verbose_name = _("Meeting External Participant")
        verbose_name_plural = _("Meeting External Participants")

    def __unicode__(self):
        return self.name

#     def natural_key(self):
#         return (self.meetings.natural_key(), self.name)
#     natural_key.dependencies = ['meetings.meeting']
