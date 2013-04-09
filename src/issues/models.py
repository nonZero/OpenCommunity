from communities.models import Community
from django.conf import settings
from django.db import models
from django.utils.translation import ugettext, ugettext_lazy as _


class Issue(models.Model):
    active = models.BooleanField(default=True, verbose_name=_("Active"))
    community = models.ForeignKey(Community, verbose_name=_("Community"), related_name="issues")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created at"))
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_("Create by"), related_name="issues_created")

    title = models.CharField(max_length=300, verbose_name=_("Title"))
    abstract = models.TextField(null=True, blank=True, verbose_name=_("Abstract"))
    content = models.TextField(null=True, blank=True, verbose_name=_("Content"))

    calculated_score = models.IntegerField(default=0, verbose_name=_("Calculated Score"))

    is_closed = models.BooleanField(default=False, verbose_name=_("Is close"))
    closed_at_meeting = models.ForeignKey('meetings.Meeting', null=True, blank=True, verbose_name=_("Closed at meeting"))
    
    class Meta:
        verbose_name = _("Issue")
        verbose_name_plural = _("Issues")

    def __unicode__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        return ("issue", (str(self.community.pk), str(self.pk), ))


class ProposalVoteValue(object):
    CON = -1
    NEUTRAL = 0
    PRO = 1

    CHOICES = (
                (CON, ugettext("Con")), 
                (NEUTRAL, ugettext("Neutral")), 
                (PRO, ugettext("Pro")),
               )


class ProposalVote(models.Model):
    proposal = models.ForeignKey("Proposal", verbose_name=_("Proposal"))
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_("User"))
    value = models.PositiveIntegerField(choices=ProposalVoteValue.CHOICES, verbose_name=_("Vote"))

    class Meta:
        unique_together = (("proposal", "user"),)
        verbose_name = _("Proposal Vote")
        verbose_name_plural = _("Proposal Votes")
        
    def __unicode__(self):
        return "%s - %s %s" % (self.proposal.issue.title, self.user.first_name, self.user.last_name)


class ProposalType(object):
    TASK = 1
    RULE = 2
    ADMIN = 3

    CHOICES = (
                (TASK, ugettext("Task")), 
                (RULE, ugettext("Rule")),
                (ADMIN, ugettext("Administrative")),
               )


class Proposal(models.Model):
    issue = models.ForeignKey(Issue, related_name="proposals", verbose_name=_("Issue"))
    active = models.BooleanField(default=True, verbose_name=_("Active"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Create at"))
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="proposals_created", verbose_name=_("Created by"))
    type = models.PositiveIntegerField(choices=ProposalType.CHOICES, verbose_name=_("Type"))

    title = models.CharField(max_length=300, verbose_name=_("Title"))
    content = models.TextField(null=True, blank=True, verbose_name=_("Content"))

    is_accepted = models.BooleanField(default=False, verbose_name=_("Is accepted"))
    accepted_at = models.DateTimeField(null=True, blank=True, verbose_name=_("Accepted at"))
    assigned_to = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_("Assigned to"), null=True, blank=True, 
                                  related_name="proposals_assigned")
    due_by = models.DateField(null=True, blank=True, verbose_name=_("Due by"))

    votes = models.ManyToManyField(settings.AUTH_USER_MODEL, verbose_name=_("Votes"), blank=True, related_name="proposals", 
                                   through="ProposalVote")

    class Meta:
        verbose_name = _("Proposal")
        verbose_name_plural = _("Proposals")

    def __unicode__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        return ("issue", (str(self.issue.community.pk), str(self.issue.pk), ))

