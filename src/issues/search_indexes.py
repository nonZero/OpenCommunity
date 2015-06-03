from haystack import indexes
from issues.models import Issue, Proposal
from haystack.fields import IntegerField, CharField, BooleanField, DateField, DateTimeField


class IssueIndex(indexes.ModelSearchIndex, indexes.Indexable):
    committee = IntegerField(model_attr='committee_id')
    is_confidential = BooleanField(model_attr='is_confidential')

    class Meta:
        model = Issue
        fields = ['title', 'abstract']

    # Note that regular ``SearchIndex`` methods apply.
    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return Issue.objects.active()


class ProposalIndex(indexes.ModelSearchIndex, indexes.Indexable):
    text = CharField(document=True, use_template=True)
    active = BooleanField(model_attr='active')
    title = CharField(model_attr='title')
    committee = IntegerField(model_attr='issue__committee_id')
    status = IntegerField(model_attr='status')
    task_completed = BooleanField(model_attr='task_completed')
    type = IntegerField(model_attr='type')
    decided_at = DateTimeField()
    assignee = CharField()
    due_by = DateField(model_attr='due_by', null=True)
    is_confidential = BooleanField(model_attr='is_confidential')

    def get_model(self):
        return Proposal

    def prepare_assignee(self, obj):
        return u'' if not obj.assigned_to_user else \
            obj.assigned_to_user.display_name

    def prepare_decided_at(self, obj):
        return obj.created_at if not obj.decided_at_meeting \
            else obj.decided_at_meeting.held_at

    # Note that regular ``SearchIndex`` methods apply.
    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return Proposal.objects.active()
