from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms
from django.utils.translation import ugettext_lazy as _
from issues import models


class CreateIssueForm(forms.ModelForm):

    class Meta:
        model = models.Issue
        fields = (
                   'title',
                   'abstract',
                   'content',
                   )

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()

        self.helper.add_input(Submit('submit', _('Create')))

        super(CreateIssueForm, self).__init__(*args, **kwargs)


class UpdateIssueForm(CreateIssueForm):
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()

        self.helper.add_input(Submit('submit', _('Update')))

        super(CreateIssueForm, self).__init__(*args, **kwargs)


class CreateProposalForm(forms.ModelForm):

    class Meta:
        model = models.Proposal
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


class CreateIssueCommentForm(forms.ModelForm):

    class Meta:
        model = models.IssueComment
        fields = (
                   'content',
                   )

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_id="add-comment"

        self.helper.add_input(Submit('submit', _('Add')))

        super(CreateIssueCommentForm, self).__init__(*args, **kwargs)

