from communities.models import Community
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms
from django.utils.translation import ugettext_lazy as _


class EditUpcomingMeetingForm(forms.ModelForm):

    class Meta:
        model = Community

        fields = (
                   'upcoming_meeting_scheduled_at',
                   'upcoming_meeting_location',
                   'upcoming_meeting_comments',
                   )

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()

        self.helper.add_input(Submit('submit', _('Submit')))

        super(EditUpcomingMeetingForm, self).__init__(*args, **kwargs)
