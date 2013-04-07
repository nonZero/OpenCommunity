from django.db import models
from django.conf import settings


class CommunityMember(models.Model):
    community = models.ForeignKey('Community')
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    is_in_board = models.BooleanField(default=False)
    is_chairman = models.BooleanField(default=False)
    is_secretary = models.BooleanField(default=False)

    class Meta:
        unique_together = (("community", "user"),)

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
    name = models.CharField(max_length=200)
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True,
                                             related_name="communities", through="CommunityMember")

    class Meta:
        verbose_name_plural = "Communities"

    def __unicode__(self):
        return self.name