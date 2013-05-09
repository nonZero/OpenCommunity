from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms
from issues.models import Issue, Proposal
from django.utils.translation import ugettext_lazy as _


class CreateIssueForm(forms.ModelForm):

    class Meta:
        model = Issue
        fields = (
                   'title',
                   'abstract',
                   'content',
                   )

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()

        self.helper.add_input(Submit('submit', _('Create')))

        super(CreateIssueForm, self).__init__(*args, **kwargs)


class CreateProposalForm(forms.ModelForm):

    class Meta:
        model = Proposal
        fields = (
                   'type',
                   'title',
                   'content',
                   'assigned_to',
                   'due_by',
                   )

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()

        self.helper.add_input(Submit('submit', _('Create')))

        super(CreateProposalForm, self).__init__(*args, **kwargs)


class EditProposalForm(CreateProposalForm):
    pass
