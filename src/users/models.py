from collections import defaultdict
from django.conf import settings
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, \
    PermissionsMixin
from django.core.mail import send_mail
from django.db import models
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _, ugettext
from users.default_roles import DefaultGroups, ALL_PERMISSIONS
import logging
import random
import string

CODE_LENGTH = 48

logger = logging.getLogger(__name__)


class OCUserManager(BaseUserManager):
    def create_user(self, email, display_name=None, password=None, **kwargs):
        """
        Creates and saves a User with the given email, display name and
        password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        if not display_name:
            display_name = email

        user = self.model(
            email=OCUserManager.normalize_email(email),
            display_name=display_name,
            **kwargs
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, display_name, password):
        """
        Creates and saves a superuser with the given email, display name and
        password.
        """
        user = self.create_user(email,
            password=password,
            display_name=display_name
        )
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class OCUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), max_length=255, unique=True,
        db_index=True,
    )
    display_name = models.CharField(_("Your name"), max_length=200)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(_('staff status'), default=False,
           help_text=_('Designates whether the user can log into this admin '
                    'site.'))
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = OCUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['display_name']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __unicode__(self):
        return self.display_name

    def get_full_name(self):
        # The user is identified by their email address
        return self.display_name

    def get_short_name(self):
        # The user is identified by their email address
        return self.display_name

    def email_user(self, subject, message, from_email=None):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email])

    _community_permissions_cache = None

    def _get_community_permissions(self, community):
        def get_permissions():
            try:
                m = self.memberships.get(community=community)
                return m.get_permissions()
            except Membership.DoesNotExist:
                return []

        if not self._community_permissions_cache:
            self._community_permissions_cache = {}

        if community.id not in self._community_permissions_cache:
            self._community_permissions_cache[community.id] = get_permissions()

        return self._community_permissions_cache[community.id]

    def has_community_perm(self, community, perm):

        if self.is_active and self.is_superuser:
            return True

        return perm in self._get_community_permissions(community)

    def get_community_perms(self, community):

        if self.is_active and self.is_superuser:
            perms = ALL_PERMISSIONS
        else:
            perms = self._get_community_permissions(community)

        d = defaultdict(dict)
        for s in perms:
            m, p = s.split('.')
            d[m][p] = True
        return d


class Membership(models.Model):
    community = models.ForeignKey('communities.Community', verbose_name=_("Community"),
                                  related_name='memberships')
    user = models.ForeignKey(OCUser, verbose_name=_("User"),
                             related_name='memberships')
    default_group_name = models.CharField(_('Group'), max_length=50,
                                          choices=DefaultGroups.CHOICES)

    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name=_("Created at"))
    invited_by = models.ForeignKey(settings.AUTH_USER_MODEL,
                                   verbose_name=_("Invited by"),
                                   related_name="members_invited", null=True,
                                   blank=True)

    class Meta:
        unique_together = (("community", "user"),)
        verbose_name = _("Community Member")
        verbose_name_plural = _("Community Members")

    def __unicode__(self):
        return "%s: %s (%s)" % (self.community.name, self.user.display_name,
                                self.get_default_group_name_display())

    def get_permissions(self):
        return DefaultGroups.permissions[self.default_group_name]

CODE_CHARS = string.lowercase + string.digits


def create_code(length=CODE_LENGTH):
    """
    Creates a random code of lowercase letters and numbers
    """
    return "".join(random.choice(CODE_CHARS) for _x in xrange(length))


class EmailStatus(object):
    PENDING = 0
    SENT = 1
    FAILED = 2

    choices = (
               (PENDING, _('Pending')),
               (SENT, _('Sent')),
               (FAILED, _('Failed')),
               )


class Invitation(models.Model):
    community = models.ForeignKey('communities.Community',
                                  verbose_name=_("Community"),
                                  related_name='invitations')

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created at"))
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL,
                                   verbose_name=_("Created by"),
                                   related_name="invitations_created")

    email = models.EmailField(_("Email"))
    message = models.TextField(_("Message"), null=True, blank=True)

    code = models.CharField(max_length=CODE_LENGTH, default=create_code)

    user = models.ForeignKey(OCUser, verbose_name=_("User"),
                             related_name='invitations', null=True, blank=True)

    default_group_name = models.CharField(_('Group'), max_length=50,
                                          choices=DefaultGroups.CHOICES)

    status = models.PositiveIntegerField(_("Status"),
                     choices=EmailStatus.choices, default=EmailStatus.PENDING)
    times_sent = models.PositiveIntegerField(_("Times Sent"), default=0)
    error_count = models.PositiveIntegerField(_("Error count"), default=0)
    last_sent_at = models.DateTimeField(_("Sent at"), null=True, blank=True)

    class Meta:
        unique_together = (("community", "email"),)

        verbose_name = _("Invitation")
        verbose_name_plural = _("Invitations")

    DEFAULT_MESSAGE = _("INVITAION_DEFAULT_MESSAGE")

    def __unicode__(self):
        return "%s: %s (%s)" % (self.community.name, self.email,
                                self.get_default_group_name_display())

    @models.permalink
    def get_absolute_url(self):
        return "accept_invitation", (self.code,)

    def send(self, base_url=None):

        if not base_url:
            base_url = settings.HOST_URL

        subject = _("Invitation to %s") % self.community.name
        d = {
              'base_url': base_url,
              'object': self,
             }

        message = render_to_string("emails/invitation.txt", d)
        recipient_list = [self.email]
        from_email = settings.FROM_EMAIL
        self.last_sent_at = timezone.now()

        try:
            send_mail(subject, message, from_email, recipient_list)
            self.times_sent += 1
            self.status = EmailStatus.SENT
            self.save()
            return True
        except:
            logger.error("Invitation email sending failed", exc_info=True)
            self.error_count += 1
            self.status = EmailStatus.ERROR
            self.save()
            return False
