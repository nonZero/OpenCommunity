from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from django.apps import AppConfig


class MeetingsConfig(AppConfig):
    name = 'meetings'
    verbose_name = _("Meetings & participants")
