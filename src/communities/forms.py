from communities.models import Community, SendToOption
from django.utils.translation import ugettext_lazy as _
from ocd.formfields import HTMLArea, DateTimeLocalInput, OCSplitDateTime
from users.models import OCUser
import floppyforms as forms


class EditUpcomingMeetingForm(forms.ModelForm):

    class Meta:
        model = Community

        fields = (
                   'upcoming_meeting_title',
                   'upcoming_meeting_scheduled_at',
                   'upcoming_meeting_location',
                   'voting_ends_at',
                   'upcoming_meeting_comments',
                   )

        widgets = {
            'upcoming_meeting_title': forms.TextInput,
            'upcoming_meeting_scheduled_at': OCSplitDateTime,
            'upcoming_meeting_location': forms.TextInput,
            'voting_ends_at': OCSplitDateTime,
            'upcoming_meeting_comments': HTMLArea,
        }
        
        
    def save(self):
        c = super(EditUpcomingMeetingForm, self).save()
        if not c.voting_ends_at:
            meeting_at = c.upcoming_meeting_scheduled_at
            if meeting_at:
                vote_ends_at = meeting_at.replace(hour=0, minute=0, second=0)
                c.voting_ends_at = vote_ends_at
                c.save()
        return c



class PublishUpcomingMeetingForm(forms.ModelForm):

    send_to = forms.TypedChoiceField(label=_("Send to"), coerce=int,
                                choices=SendToOption.choices,
                                widget=forms.RadioSelect)

    class Meta:
        model = Community

        fields = ()


class EditUpcomingMeetingSummaryForm(forms.ModelForm):

    class Meta:
        model = Community

        fields = (
                   'upcoming_meeting_summary',
                   )

        widgets = {
            'upcoming_meeting_summary': HTMLArea,
        }



class StartMeetingForm(forms.ModelForm):

    class Meta:
        model = Community

        fields = (
                  'upcoming_meeting_started',
                  )

        widgets = {
            'upcoming_meeting_started': forms.CheckboxInput,
        }


class UpcomingMeetingParticipantsForm(forms.ModelForm):

#     upcoming_meeting_participants = forms.ModelMultipleChoiceField(label=_(
#                                          "Participants in upcoming meeting"),
#                                        required=False,
#                                        queryset=OCUser.objects.all(),
#                                        widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = Community

        fields = (
                   'upcoming_meeting_participants',
                   'upcoming_meeting_guests',
                   )

        widgets = {
            'upcoming_meeting_participants': forms.CheckboxSelectMultiple,
            'upcoming_meeting_guests': forms.Textarea,
        }

    def __init__(self, *args, **kwargs):
        super(UpcomingMeetingParticipantsForm, self).__init__(*args, **kwargs)
        self.fields['upcoming_meeting_participants'].queryset = self.instance.get_members()

