from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from django.apps import AppConfig


class IssuesConfig(AppConfig):
    name = 'issues'
    verbose_name = _("Issues, proposals & votes")
