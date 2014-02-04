from communities.models import Community, SendToOption
from datetime import datetime, date, time
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from ocd import formfields
from ocd.formfields import HTMLArea, OCSplitDateTime
import floppyforms as forms

class EditUpcomingMeetingForm(forms.ModelForm):

    class Meta:
        model = Community

        fields = (
                   'upcoming_meeting_title',
                   'upcoming_meeting_location',
                   'upcoming_meeting_scheduled_at',
                   # 'voting_ends_at',
                   'upcoming_meeting_comments',
                   )

        widgets = {
            'upcoming_meeting_title': forms.TextInput,
            'upcoming_meeting_scheduled_at': OCSplitDateTime,
            'upcoming_meeting_location': forms.TextInput,
            # 'voting_ends_at': OCSplitDateTime,
            'upcoming_meeting_comments': HTMLArea,
        }
        
    def __init__(self, *args, **kwargs):
        super(EditUpcomingMeetingForm, self).__init__(*args, **kwargs)
        self.fields['upcoming_meeting_title'].label = _('Title')
        self.fields['upcoming_meeting_scheduled_at'].label = _('Scheduled at')
        self.fields['upcoming_meeting_location'].label = _('Location')
        self.fields['upcoming_meeting_comments'].label = _('Background')

    """
    removed this function as we don't include voting_end_time in the form any more.
    # ----------------------------------------------------------------------------
    def clean(self):
        #prevent voting end time from illegal values (past time,
        #time after meeting schedule)
        
        try:
            voting_ends_at = self.cleaned_data['voting_ends_at']
        except KeyError:
            voting_ends_at = None
        try:
            meeting_time = self.cleaned_data['upcoming_meeting_scheduled_at']
        except KeyError:
            meeting_time = None

        if voting_ends_at:
            if voting_ends_at <= timezone.now():
                raise forms.ValidationError(_("End voting time cannot be set to the past"))
            if meeting_time and voting_ends_at > meeting_time:
                raise forms.ValidationError(_("End voting time cannot be set to after the meeting time"))
        return self.cleaned_data
    """
            
    def save(self):
        c = super(EditUpcomingMeetingForm, self).save()
        c.voting_ends_at = datetime.combine(date(2025, 1, 1), time(12, 0, 0))
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


class UpcomingMeetingParticipantsForm(forms.ModelForm):

    class Meta:
        model = Community

        fields = (
                   'upcoming_meeting_participants',
                   'upcoming_meeting_guests',
                   )

        widgets = {
            'upcoming_meeting_participants': formfields.OCCheckboxSelectMultiple,
             'upcoming_meeting_guests': forms.Textarea,
        }
    
    def __init__(self, *args, **kwargs):
        super(UpcomingMeetingParticipantsForm, self).__init__(*args, **kwargs)
        self.fields['upcoming_meeting_participants'].label = ""
#         self.fields['upcoming_meeting_guests'].widget.attrs['rows'] = 4
