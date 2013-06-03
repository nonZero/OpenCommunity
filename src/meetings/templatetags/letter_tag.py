from django import template
from django.utils.translation import ugettext_lazy as _

LETTERS = [_("a"), _("b"), _("c"), _("d"), _("e"),
           _("f"), _("g"), _("h"), _("i"), _("j")]

register = template.Library()


@register.filter
def to_char(value):
    if value > len(LETTERS):
        return value
    return LETTERS[value - 1]
