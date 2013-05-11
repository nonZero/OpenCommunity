from crispy_forms.helper import FormHelper
from django import forms
from django.utils.translation import ugettext_lazy as _
from meetings.models import Meeting
from crispy_forms.layout import Submit


class CloseMeetingForm(forms.ModelForm):

    class Meta:
        model = Meeting

        fields = ('held_at', 'summary',)

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()

        self.helper.add_input(Submit('submit', _('Close Meeting')))

        super(CloseMeetingForm, self).__init__(*args, **kwargs)
