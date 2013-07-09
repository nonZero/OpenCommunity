from communities.models import SendToOption
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms
from django.utils.translation import ugettext_lazy as _
from meetings.models import Meeting


class CloseMeetingForm(forms.ModelForm):

    send_to = forms.TypedChoiceField(label=_("Send to"), coerce=int,
                                choices=SendToOption.choices[2:],
                                widget=forms.RadioSelect)

    class Meta:
        model = Meeting

        fields = (
                  'held_at',
                  )

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()

        self.helper.add_input(Submit('submit', _('Close Meeting')))

        super(CloseMeetingForm, self).__init__(*args, **kwargs)
