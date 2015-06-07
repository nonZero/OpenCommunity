from django.core.urlresolvers import reverse
from django.db import models
from django.utils.translation import ugettext_lazy as _
from acl import core_permissions
from acl.default_roles import DefaultRoles


class Role(models.Model):
    community = models.ForeignKey('communities.Community', null=True,
                                  blank=True,
                                  verbose_name=_("Limit to community"))
    ordinal = models.IntegerField(_("ordinal"), default=0)
    title = models.CharField(_("title"), max_length=200, unique=True)
    based_on = models.CharField(_("based on"), max_length=50, null=True,
                                blank=True, choices=DefaultRoles.choices)

    def get_absolute_url(self):
        return reverse('role:view', kwargs={'pk': self.id})

    def __unicode__(self):
        return self.title

    def all_perms(self):
        perms = set()
        if self.based_on:
            perms.update(DefaultRoles.permissions[self.based_on])
        perms.update(self.perms.values_list('code', flat=True))
        return sorted(perms, key=lambda p: core_permissions.ORDER[p])

    def all_perms_titles(self):
        return [core_permissions.CHOICES_DICT[p] for p in self.all_perms()]


class RolePermission(models.Model):
    role = models.ForeignKey(Role, related_name='perms')
    code = models.CharField(_('Permission'), max_length=100,
                            choices=core_permissions.CHOICES)

    class Meta:
        unique_together = (
            ('role', 'code'),
        )

    def __unicode__(self):
        return self.get_code_display()
