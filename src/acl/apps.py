from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from django.apps import AppConfig


class AclConfig(AppConfig):
    name = 'acl'
    verbose_name = _("Access Control Logic")
