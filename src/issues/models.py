from django.conf import settings
from django.db import models, transaction
from django.utils import timezone
from django.utils.text import get_valid_filename

from django.utils.translation import ugettext, ugettext_lazy as _
from ocd.base_models import HTMLField, UIDMixin, UIDManager
from ocd.validation import enhance_html

import os.path

class IssueStatus(object):

    OPEN = 1
    IN_UPCOMING_MEETING = 2
    IN_UPCOMING_MEETING_COMPLETED = 3  # currently unused!
    ARCHIVED = 4

    choices = (
               (OPEN, _('Open')),
               (IN_UPCOMING_MEETING, _('In upcoming meeting')),
               (IN_UPCOMING_MEETING_COMPLETED, _('In upcoming meeting (completed)')),
               (ARCHIVED, _('Archived')),
               )

    IS_UPCOMING = (IN_UPCOMING_MEETING, IN_UPCOMING_MEETING_COMPLETED)
    NOT_IS_UPCOMING = (OPEN, ARCHIVED)


class Issue(UIDMixin):
    active = models.BooleanField(default=True, verbose_name=_("Active"))
    community = models.ForeignKey('communities.Community', verbose_name=_("Community"), related_name="issues")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created at"))
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_("Create by"), related_name="issues_created")

    title = models.CharField(max_length=300, verbose_name=_("Title"))
    abstract = HTMLField(null=True, blank=True, verbose_name=_("Background"))
    content = HTMLField(null=True, blank=True, verbose_name=_("Content"))

    calculated_score = models.IntegerField(default=0, verbose_name=_("Calculated Score"))

    status = models.IntegerField(choices=IssueStatus.choices,
                                 default=IssueStatus.OPEN)
    statuses = IssueStatus

#     in_upcoming_meeting = models.BooleanField(_("In upcoming meeting"), default=False)
    order_in_upcoming_meeting = models.IntegerField(
                                        _("Order in upcoming meeting"),
                                        default=9999, null=True, blank=True)
    length_in_minutes = models.IntegerField(_("Length (in minutes)"),
                                            null=True, blank=True)

    completed = models.BooleanField(default=False,
                                    verbose_name=_("Discussion completed"))
    is_published = models.BooleanField(_("Is published to members"),
                                       default=False)

    class Meta:
        verbose_name = _("Issue")
        verbose_name_plural = _("Issues")

    def __unicode__(self):
        return self.title

    @models.permalink
    def get_edit_url(self):
        return ("issue_edit", (str(self.community.pk), str(self.pk),))

    @models.permalink
    def get_delete_url(self):
        return ("issue_delete", (str(self.community.pk), str(self.pk),))

    @models.permalink
    def get_absolute_url(self):
        return ("issue", (str(self.community.pk), str(self.pk),))

    def active_proposals(self):
        return self.proposals.filter(active=True)

    def new_comments(self):
        return self.comments.filter(active=True, meeting_id=None)

    def has_closed_parts(self):
        """ Should be able to be viewed """

    @property
    def is_upcoming(self):
        return self.status in IssueStatus.IS_UPCOMING

    @property
    def is_archived(self):
        return self.status == IssueStatus.ARCHIVED


class IssueComment(UIDMixin):
    issue = models.ForeignKey(Issue, related_name="comments")
    active = models.BooleanField(default=True)
    ordinal = models.PositiveIntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name=_("Created at"))
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL,
                                   verbose_name=_("Created by"),
                                   related_name="issue_comments_created")

    meeting = models.ForeignKey('meetings.Meeting', null=True, blank=True)

    version = models.PositiveIntegerField(default=1)
    last_edited_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name=_("Last Edited at"))
    last_edited_by = models.ForeignKey(settings.AUTH_USER_MODEL,
                                   verbose_name=_("Created by"),
                                   related_name="issue_comments_last_edited",
                                   null=True, blank=True)
    content = HTMLField(verbose_name=_("Comment"))

    class Meta:
        ordering = ('created_at',)

    @property
    def is_open(self):
        return self.meeting_id is None

    def update_content(self, expected_version, author, content):
        """ creates a new revision and updates current comment """
        if self.version != expected_version:
            return False

        content = enhance_html(content.strip())

        if self.content == content:
            return True

        with transaction.commit_on_success():
            IssueCommentRevision.objects.create(comment=self,
                                                version=expected_version,
                                                created_at=self.created_at,
                                                created_by=self.created_by,
                                                content=self.content)
            self.version += 1
            self.last_edited_at = timezone.now()
            self.last_edited_by = author
            self.content = content
            self.save()

        return True

    @models.permalink
    def get_delete_url(self):
        return "delete_issue_comment", (self.issue.community.id, self.id)

    @models.permalink
    def get_edit_url(self):
        return "edit_issue_comment", (self.issue.community.id, self.id)


class IssueCommentRevision(models.Model):
    """ Holds data for historical comments """
    comment = models.ForeignKey(IssueComment, related_name='revisions')
    version = models.PositiveIntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name=_("Created at"))
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL,
                               verbose_name=_("Created by"),
                               related_name="issue_comment_versions_created")

    content = models.TextField(verbose_name=_("Content"))

    
def issue_attachment_path(instance, filename):
    filename = get_valid_filename(os.path.basename(filename))
    return os.path.join(instance.issue.community.uid, instance.issue.uid, filename)

    
class IssueAttachment(UIDMixin):
    issue = models.ForeignKey(Issue, related_name="attachments")
    file = models.FileField(upload_to=issue_attachment_path)
    title = models.CharField(max_length=100)
    active = models.BooleanField(default=True)
    ordinal = models.PositiveIntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name=_("File created at"))
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL,
                                   verbose_name=_("Created by"),
                                   related_name="files_created")

    class Meta:       
        ordering = ('created_at', )

        
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
        return "%s - %s" % (self.proposal.issue.title, self.user.display_name)


class ProposalType(object):
    TASK = 1
    RULE = 2
    ADMIN = 3

    CHOICES = (
                (TASK, ugettext("Task")),
                (RULE, ugettext("Rule")),
                (ADMIN, ugettext("General")),
               )


class ProposalManager(UIDManager):

    def active(self):
        return self.get_query_set().filter(active=True)

    def open(self):
        return self.get_query_set().filter(active=True,
                                           decided_at_meeting_id=None)

    def closed(self):
        return self.get_query_set().filter(active=True).exclude(
                                                    decided_at_meeting_id=None)


class ProposalStatus(object):
    IN_DISCUSSION = 1
    ACCEPTED = 2
    REJECTED = 3

    choices = (
               (IN_DISCUSSION, _('In discussion')),
               (ACCEPTED, _('Accepted')),
               (REJECTED, _('Rejected')),
              )


class Proposal(UIDMixin):
    issue = models.ForeignKey(Issue, related_name="proposals",
                              verbose_name=_("Issue"))
    active = models.BooleanField(_("Active"), default=True)
    created_at = models.DateTimeField(_("Create at"), auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL,
                                   related_name="proposals_created",
                                   verbose_name=_("Created by"))
    type = models.PositiveIntegerField(_("Type"), choices=ProposalType.CHOICES)
    types = ProposalType

    title = models.CharField(_("Title"), max_length=300)
    content = HTMLField(_("Content"), null=True, blank=True)

    status = models.IntegerField(choices=ProposalStatus.choices,
                                 default=ProposalStatus.IN_DISCUSSION)
    statuses = ProposalStatus

    decided_at_meeting = models.ForeignKey('meetings.Meeting', null=True, blank=True)
    assigned_to = models.CharField(_("Assigned to"), max_length=200,
                                   null=True, blank=True)
    assigned_to_user = models.ForeignKey(settings.AUTH_USER_MODEL,
                                         verbose_name=_("Assigned to user"),
                                         null=True, blank=True,
                                         related_name="proposals_assigned")
    due_by = models.DateField(_("Due by"), null=True, blank=True)

    votes = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                   verbose_name=_("Votes"), blank=True,
                                   related_name="proposals",
                                   through="ProposalVote")

    objects = ProposalManager()

    class Meta:
        verbose_name = _("Proposal")
        verbose_name_plural = _("Proposals")

    def __unicode__(self):
        return self.title

    @property
    def is_open(self):
        return self.decided_at_meeting is None

    @property
    def can_vote(self):
        """ Returns True if the proposal, issue and meeting are open """
        print "xyz", self.id, self.is_open, self.issue.is_upcoming, \
                   self.issue.community.upcoming_meeting_started
        return self.is_open and self.issue.is_upcoming and \
                   self.issue.community.upcoming_meeting_started

    def is_task(self):
        return self.type == ProposalType.TASK

    @models.permalink
    def get_absolute_url(self):
        return ("proposal", (str(self.issue.community.pk), str(self.issue.pk),
                                str(self.pk)))

    @models.permalink
    def get_edit_url(self):
        return ("proposal_edit", (str(self.issue.community.pk), str(self.issue.pk),
                                str(self.pk)))

    @models.permalink
    def get_edit_task_url(self):
        return ("proposal_edit_task", (str(self.issue.community.pk), str(self.issue.pk),
                                str(self.pk)))

    @models.permalink
    def get_delete_url(self):
        return ("proposal_delete", (str(self.issue.community.pk), str(self.issue.pk),
                                str(self.pk)))

