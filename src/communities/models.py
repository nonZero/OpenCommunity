from django.conf import settings
from django.db import models
from django.utils.translation import ugettext, ugettext_lazy as _


class CommunityMember(models.Model):
    community = models.ForeignKey('Community', verbose_name=_("Community"))
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_("User"))
    is_in_board = models.BooleanField(default=False, verbose_name=_("Is In Board"))
    is_chairman = models.BooleanField(default=False, verbose_name=_("Is Chairman"))
    is_secretary = models.BooleanField(default=False, verbose_name=_("Is Secretary"))

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
        return "%s: %s (%s)" % (self.community.name, self.user.username, self.member_type_as_string())


class Community(models.Model):
    name = models.CharField(max_length=200, verbose_name=_("Name"))
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, verbose_name=_("Members"),
                                             related_name="communities", through="CommunityMember")

    class Meta:
        verbose_name = _("Community")
        verbose_name_plural = _("Communities")

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ("community", (str(self.pk,)))