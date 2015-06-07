from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class AclConfig(AppConfig):
    name = 'acl'
    verbose_name = _("Access Control Logic")
