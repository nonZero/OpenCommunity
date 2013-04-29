from django.conf import settings
from django.db import models
from django.utils.translation import ugettext, ugettext_lazy as _


class CommunityMember(models.Model):
    community = models.ForeignKey('Community', verbose_name=_("Community"))
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_("User"))
    is_in_board = models.BooleanField(_("Is In Board"), default=False)
    is_chairman = models.BooleanField(_("Is Chairman"), default=False)
    is_secretary = models.BooleanField(_("Is Secretary"), default=False)

    class Meta:
        unique_together = (("community", "user"),)
        verbose_name = _("Community Member")
        verbose_name_plural = _("Community Members")

    def member_type_as_string(self):
        titles = []
        if self.is_in_board:
            titles.append("Board Member")
        if self.is_chairman:
            titles.append("Chairman")
        if self.is_secretary:
            titles.append("Secretary")

        return ", ".join(titles) if titles else "Regular Member"

    def __unicode__(self):
        return "%s: %s (%s)" % (self.community.name, self.user.username,
                                self.member_type_as_string())


class Community(models.Model):
    name = models.CharField(max_length=200, verbose_name=_("Name"))
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True,
                                     verbose_name=_("Members"),
                                     related_name="communities",
                                     through="CommunityMember")

    upcoming_meeting_scheduled_at = models.DateTimeField(
                                        _("Upcoming meeting scheduled at"),
                                        blank=True, null=True)
    upcoming_meeting_location = models.CharField(
                                         _("Upcoming meeting location"),
                                         max_length=300, null=True,
                                         blank=True)
    upcoming_meeting_comments = models.TextField(
                                             _("Upcoming meeting comments"),
                                             null=True, blank=True)

    upcoming_meeting_participants = models.ManyToManyField(
                                      settings.AUTH_USER_MODEL,
                                      blank=True,
                                      related_name="+",
                                      verbose_name=_(
                                         "Participants in upcoming meeting"))

    upcoming_meeting_version = models.IntegerField(
                                   _("Upcoming meeting version"), default=0)

    upcoming_meeting_is_published = models.BooleanField(
                                        _("Upcoming meeting is published"),
                                        default=False)
    upcoming_meeting_published_at = models.DateTimeField(
                                        _("Upcoming meeting published at"),
                                        blank=True, null=True)

    class Meta:
        verbose_name = _("Community")
        verbose_name_plural = _("Communities")

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ("community", (str(self.pk,)))

    @models.permalink
    def get_upcoming_absolute_url(self):
        return ("upcoming_meeting", (str(self.pk,)))

    def upcoming_issues(self, upcoming=True):
        return self.issues.filter(active=True, is_closed=False,
                                  in_upcoming_meeting=upcoming)

    def available_issues(self):
        return self.upcoming_issues(False)

    def issues_ready_to_close(self):
        return self.upcoming_issues().filter(
                                         proposals__is_accepted=True
                                     ).annotate(
                                        num_proposals=models.Count('proposals')
                                     )
