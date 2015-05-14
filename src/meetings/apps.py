from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class MeetingsConfig(AppConfig):
    name = 'meetings'
    verbose_name = _("Meetings & participants")
