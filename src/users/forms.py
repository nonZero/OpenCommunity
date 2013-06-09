from django.forms.models import ModelForm
from users.models import Invitation


class InvitationForm(ModelForm):

    class Meta:
        model = Invitation

        fields = (
                  'email',
                  'default_group_name',
                  )
