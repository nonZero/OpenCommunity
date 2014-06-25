from acl import core_permissions, models
import floppyforms as forms
from ocd.formfields import OCCheckboxSelectMultiple


class RoleForm(forms.ModelForm):
    perms = forms.MultipleChoiceField(required=False,
                                      choices=core_permissions.CHOICES,
                                      widget=OCCheckboxSelectMultiple)

    class Meta:
        model = models.Role
        fields = (
            'title',
            'based_on',
        )
        widgets = {
            'title': forms.TextInput,
            'based_on': forms.Select,
        }
