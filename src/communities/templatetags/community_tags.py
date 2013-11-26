from django import template
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext, ugettext_lazy as _
from datetime import datetime, time
from django.utils import timezone

from users.models import Membership

register = template.Library()

@register.filter
def display_upcoming_time(community):
    """ display only date if hour information if not set (remains at default '00:00)
    """
    if not community.upcoming_meeting_scheduled_at:
        return _("Not set yet")
    when = timezone.localtime(community.upcoming_meeting_scheduled_at)
    t = when.timetz()
    if t.hour == 0 and t.minute == 0:
        return when.date()
    else:
        return when

        
@register.filter
def member_of(u, community):
    res = Membership.objects.filter(user=u)
    for membership in res:
        if membership.community == community:
            return True
    return False