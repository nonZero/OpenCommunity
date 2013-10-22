#from django import forms
#from django.forms.models import ModelForm
from django.utils.translation import ugettext_lazy as _
from ocd.formfields import HTMLArea
from users.models import Invitation, OCUser
import floppyforms as forms


class InvitationForm(forms.ModelForm):

    class Meta:
        model = Invitation

        fields = (
                  'email',
                  'default_group_name',
                  'message',
                  )

        widgets = {
            'default_group_name': forms.Select,
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

