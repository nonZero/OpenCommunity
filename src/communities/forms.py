from communities.models import Community
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms
from django.utils.translation import ugettext_lazy as _
from users.models import OCUser


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

        self.helper.add_input(Submit('submit', _('Save')))

        super(EditUpcomingMeetingForm, self).__init__(*args, **kwargs)


class PublishUpcomingMeetingForm(forms.ModelForm):

    send_to_members = forms.BooleanField(False,
                                         label=_("Send to All Members"))
    send_to_board = forms.BooleanField(False,
                                       label=_("Send to Board"))

    class Meta:
        model = Community

        fields = ()

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        attrs={'data-rel':'back'}
        self.helper.add_input(Submit('submit', _('Publish'), **attrs))

        super(PublishUpcomingMeetingForm, self).__init__(*args, **kwargs)


class UpcomingMeetingParticipantsForm(forms.ModelForm):

    upcoming_meeting_participants = forms.ModelMultipleChoiceField(label=_(
                                         "Participants in upcoming meeting"),
                                       required=False,
                                       queryset=OCUser.objects.all(),
                                       widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = Community

        fields = (
                   'upcoming_meeting_participants',
                   'upcoming_meeting_guests',
                   )

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()

        self.helper.add_input(Submit('submit', _('Save')))

        super(UpcomingMeetingParticipantsForm, self).__init__(*args, **kwargs)

        self.fields['upcoming_meeting_participants'].queryset = self.instance.get_members()

