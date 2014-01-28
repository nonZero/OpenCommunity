#from django import forms
#from django.forms.models import ModelForm
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from django.utils.translation import ugettext_lazy as _
from ocd.formfields import HTMLArea
from users.models import Invitation, OCUser
import floppyforms as forms


LOGIN_ERROR = _("Please enter a correct %(username)s and password. "
                           "Note that both fields may be case-sensitive.")

class InvitationForm(forms.ModelForm):

    class Meta:
        model = Invitation

        fields = (
                  'name',
                  'email',
                  'default_group_name',
                  'message',
                  )

        widgets = {
            'default_group_name': forms.Select,
            'name': forms.TextInput,
            'email': forms.EmailInput,
            'message': HTMLArea,
        }
    
    def clean_email(self):
        return self.cleaned_data.get("email").lower()


class QuickSignupForm(forms.ModelForm):

    password1 = forms.CharField(label=_('Password'), widget=forms.PasswordInput)
    password2 = forms.CharField(label=_('Password confirmation'), widget=forms.PasswordInput)

    class Meta:
        model = OCUser

        fields = (
                  'display_name',
                  )

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(_("Passwords don't match"))
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(QuickSignupForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class OCPasswordResetForm(PasswordResetForm):

    class Meta:
        fields = (
                  'email',
                  )

    def __init__(self, *args, **kwargs):
        super(OCPasswordResetForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs['class'] = u'form-control'
        
class OCPasswordResetConfirmForm(SetPasswordForm):

    class Meta:
        fields = (
                  'new_password1',
                  'new_password2',
                  )

    def __init__(self, *args, **kwargs):
        super(OCPasswordResetConfirmForm, self).__init__(*args, **kwargs)
        self.fields['new_password1'].widget.attrs['class'] = u'form-control'
        self.fields['new_password2'].widget.attrs['class'] = u'form-control'


class ImportInvitationsForm(forms.Form):
    csv_file = forms.FileField(required=True)

        
