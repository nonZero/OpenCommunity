from haystack import indexes
from issues.models import Issue, Proposal
from haystack.fields import IntegerField, CharField, BooleanField, DateTimeField


class IssueIndex(indexes.ModelSearchIndex, indexes.Indexable):
    community = IntegerField(model_attr='community_id')
    class Meta:
        model = Issue
        fields = ['title', 'abstract']

    # Note that regular ``SearchIndex`` methods apply.
    def index_queryset(self, using=None):
        "Used when the entire index for model is updated."
        return Issue.objects.all()


class ProposalIndex(indexes.ModelSearchIndex, indexes.Indexable):
    text = CharField(document=True, use_template=True)
    active = BooleanField(model_attr='active')
    title = CharField(model_attr='title')
    community = IntegerField(model_attr='issue__community_id')
    status = IntegerField(model_attr='status')
    type = IntegerField(model_attr='type')
    created_at = DateTimeField(model_attr='created_at')
    # tags = CharField(model_attr='tags')
    # procedure_rendered = CharField(use_template=True, indexed=False)

    def get_model(self):
        return Proposal
    """
    def prepare_tags(self, obj):
        return ' '.join(obj.tags.names())
    """

    # Note that regular ``SearchIndex`` methods apply.
    def index_queryset(self, using=None):
        "Used when the entire index for model is updated."
        return Proposal.objects.all()
