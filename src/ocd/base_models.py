from django.db import models
from ocd.validation import enhance_html
from django.utils.translation import ugettext_lazy as _


class HTMLField(models.TextField):
    """
    A string field for HTML content.
    """
    description = _("HTML content")

    def formfield(self, **kwargs):
        ff = super(HTMLField, self).formfield(**kwargs)
        if 'class' in ff.widget.attrs:
            ff.widget.attrs['class'] += " wysiwyg"
        else:
            ff.widget.attrs['class'] = "wysiwyg"
        return ff

    def clean(self, value, model_instance):
        value = super(HTMLField, self).clean(value, model_instance)
        return enhance_html(value)

try:
    from south.modelsinspector import add_introspection_rules
    add_introspection_rules([], ["^ocd\.base_models\.HTMLField"])
except ImportError:
    pass
