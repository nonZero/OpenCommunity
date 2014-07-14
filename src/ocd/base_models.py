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


class ConfidentialMixin(models.Model):

    class Meta:
        abstract = True

    confidential_reason = models.ForeignKey(
        'communities.CommunityConfidentialReason',
        blank=True,
        null=True,)

    is_confidential = models.BooleanField(
        _('Is Confidential'),
        default=False,
        editable=False,)

    def enforce_confidential_rules(self):
        if self.confidential_reason is None:
            self.is_confidential = False
        else:
            self.is_confidential = True

    def save(self, *args, **kwargs):
        self.enforce_confidential_rules()
        return super(ConfidentialMixin, self).save(*args, **kwargs)


class ConfidentialByRelationMixin(models.Model):

    confidential_from = None

    class Meta:
        abstract = True

    is_confidential = models.BooleanField(
        _('Is Confidential'),
        default=False,
        editable=False,)

    def enforce_confidential_rules(self):
        if not self.confidential_from:
            # if the model is misconfigured in any way with respect to
            # confidentiality, we want to raise an error here.
            raise ValueError(_('Models with ConfidentialByRelationMixin must '
                               'declare a valid field which can pass on'
                               'confidentiality.'))

        else:
            # things seem good, so let's apply the confidential object logic.
            confidential_relation = getattr(self, self.confidential_from)

            if confidential_relation.is_confidential is True:
                # when the confidential_relation is True, this *must* be true.
                self.is_confidential = True
            else:
                self.is_confidential = False

    def save(self, *args, **kwargs):
        self.enforce_confidential_rules()
        return super(ConfidentialByRelationMixin, self).save(*args, **kwargs)
