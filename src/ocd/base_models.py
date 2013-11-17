from django.db import models
from django.utils.translation import ugettext_lazy as _
from ocd.validation import enhance_html
import random
import string


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


UID_CHARS = string.lowercase + string.digits
UID_LENGTH = 24


def create_uid(length=UID_LENGTH):
    """
    Creates a random code of lowercase letters and numbers
    """
    return "".join(random.choice(UID_CHARS) for _x in xrange(length))


class UIDManager(models.Manager):
    def get_by_natural_key(self, uid):
        return self.get(uid=uid)


class UIDMixin(models.Model):

    uid = models.CharField(max_length=UID_LENGTH, unique=True,
                           default=create_uid)

    objects = UIDManager()

    def natural_key(self):
        return (self.uid,)

    class Meta:
        abstract = True

