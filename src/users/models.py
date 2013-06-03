from communities.models import Community
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, \
    PermissionsMixin
from django.core.mail import send_mail
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from users.default_roles import DefaultGroups, ALL_PERMISSIONS
from collections import defaultdict


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
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
        db_index=True,
    )
    display_name = models.CharField(max_length=200)
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
        return self.email

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

    class Meta:
        unique_together = (("community", "user"),)
        verbose_name = _("Community Member")
        verbose_name_plural = _("Community Members")

    def __unicode__(self):
        return "%s: %s (%s)" % (self.community.name, self.user.display_name,
                                self.get_default_group_name_display())

    def get_permissions(self):
        return DefaultGroups.permissions[self.default_group_name]
