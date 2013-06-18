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

class DeleteIssueForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()

        self.helper.add_input(Submit('submit', _('Delete')))
        
        super(CreateIssueForm, self).__init__(*args, **kwargs)

class CreateProposalForm(forms.ModelForm):

    submit_button_text = _('Create')

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

        self.helper.add_input(Submit('submit', self.submit_button_text))

        super(CreateProposalForm, self).__init__(*args, **kwargs)


class EditProposalForm(CreateProposalForm):
    submit_button_text = _('Save')


class EditProposalTaskForm(EditProposalForm):

    class Meta:
        model = models.Proposal
        fields = (
                   'assigned_to',
                   'due_by',
                   )


class CreateIssueCommentForm(forms.ModelForm):

    submit_label = _('Add')
    form_id = "add-comment"

    class Meta:
        model = models.IssueComment
        fields = (
                   'content',
                   )

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        if self.form_id:
            self.helper.form_id = self.form_id

        self.helper.add_input(Submit('submit', self.submit_label))

        super(CreateIssueCommentForm, self).__init__(*args, **kwargs)


class EditIssueCommentForm(CreateIssueCommentForm):

    submit_label = _('Save')
    form_id = None
