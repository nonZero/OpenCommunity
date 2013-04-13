from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms
from django.utils.translation import ugettext_lazy as _
from meetings.models import Meeting


class CreateMeetingForm(forms.ModelForm):

    class Meta:
        model = Meeting
        fields = (
                   'scheduled_at',
                   'location',
                   'comments',
                   )

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()

        self.helper.add_input(Submit('submit', _('Submit')))

        super(CreateMeetingForm, self).__init__(*args, **kwargs)

