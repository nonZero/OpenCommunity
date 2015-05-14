from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class IssuesConfig(AppConfig):
    name = 'issues'
    verbose_name = _("Issues, proposals & votes")
