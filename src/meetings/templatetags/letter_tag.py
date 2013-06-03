from django import template
from django.utils.translation import ugettext_lazy as _


# Just to get hebrew letters translated, not is any other use elsewhere.
LETTERS = [_("a"),_("b"),_("c"),_("d"),_("e"),_("f"),_("g"),_("h"),_("i"),_("j")]


register = template.Library()

@register.filter
def to_char(value):
    return _(chr(96+value))
