from communities.models import SendToOption
from django import forms
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from meetings.models import Meeting


class CloseMeetingForm(forms.ModelForm):

    send_to_options = list(SendToOption.choices[2:])

    # On QA servers, allow users to prevent sending of protocols
    if settings.QA_SERVER:
        send_to_options.insert(0, SendToOption.choices[0])

    send_to = forms.TypedChoiceField(label=_("Send to"), coerce=int,
                                     choices=send_to_options,
                                     widget=forms.RadioSelect)

    class Meta:
        model = Meeting

        fields = (
                  'held_at',
                  )

    def __init__(self, *args, **kwargs):
#         self.helper = FormHelper()
# 
#         self.helper.add_input(Submit('submit', _('Close Meeting')))

        super(CloseMeetingForm, self).__init__(*args, **kwargs)
