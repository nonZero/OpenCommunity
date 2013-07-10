from django.http.response import HttpResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from issues import models, forms
from issues.forms import CreateIssueForm, CreateProposalForm, EditProposalForm, \
    UpdateIssueForm, EditProposalTaskForm
from issues.models import ProposalType
from ocd.base_views import CommunityMixin, AjaxFormView
import datetime
import json


class IssueMixin(CommunityMixin):

    model = models.Issue

    def get_queryset(self):
        return models.Issue.objects.filter(community=self.community,
                                           active=True)


class IssueList(IssueMixin, ListView):

    required_permission = 'issues.viewopen_issue'

    def get_queryset(self):
        return super(IssueList, self).get_queryset().filter(
              is_closed=False).order_by('-in_upcoming_meeting', '-created_at')


class IssueDetailView(IssueMixin, DetailView):

    def get_required_permission(self):
        o = self.get_object()
        return 'issues.viewclosed_issue' if o.is_closed else 'issues.viewopen_issue'

    def get_context_data(self, **kwargs):
        d = super(IssueDetailView, self).get_context_data(**kwargs)
        d['form'] = forms.CreateIssueCommentForm()
        return d

    required_permission_for_post = 'issues.add_issuecomment'

    def post(self, request, *args, **kwargs):

        form = forms.CreateIssueCommentForm(request.POST)
        if not form.is_valid():
            return HttpResponseBadRequest()

        i = self.get_object()
        c = i.comments.create(content=form.cleaned_data['content'],
                              created_by=request.user)

        cperms = self.request.user.get_community_perms(self.community)

        return render(request, 'issues/_comment.html', {
                                                        'c': c,
                                                        'object': i,
                                                        'cperms': cperms,
                                                        })


class IssueCommentMixin(CommunityMixin):
    model = models.IssueComment

    def get_required_permission(self):
        o = self.get_object()
        return 'issues.editopen_issuecomment' if o.issue.is_closed else \
            'issues.editclosed_issuecomment'

    def get_queryset(self):
        return models.IssueComment.objects.filter(issue__community=self.community)


class IssueCommentDeleteView(IssueCommentMixin, DeleteView):

    def post(self, request, *args, **kwargs):
        o = self.get_object()
        o.active = 'undelete' in request.POST
        o.save()
        return HttpResponse(int(o.active))


class IssueCommentEditView(IssueCommentMixin, UpdateView):

    form_class = forms.EditIssueCommentForm

    def form_valid(self, form):
        c = self.get_object()
        c.update_content(form.instance.version, self.request.user,
                                     form.cleaned_data['content'])
        cperms = self.request.user.get_community_perms(self.community)

        return render(self.request, 'issues/_comment.html', {
                                                        'c': c,
                                                        'object': c.issue,
                                                        'cperms': cperms,
                                                        })

    def form_invalid(self, form):
        return HttpResponse("")

    def get_form_kwargs(self):
        d = super(IssueCommentEditView, self).get_form_kwargs()
        d['prefix'] = 'ic%d' % self.get_object().id
        return d


class IssueCreateView(AjaxFormView, IssueMixin, CreateView):
    form_class = CreateIssueForm
    template_name="issues/issue_create_form.html"

    required_permission = 'issues.add_issue'

    def form_valid(self, form):
        form.instance.community = self.community
        form.instance.created_by = self.request.user
        return super(IssueCreateView, self).form_valid(form)


class IssueEditView(AjaxFormView, IssueMixin, UpdateView):

    reload_on_success = True

    required_permission = 'issues.editopen_issue'

    form_class = UpdateIssueForm


class IssueDeleteView(AjaxFormView, IssueMixin, DeleteView):

    def get_required_permission(self):
        o = self.get_object()
        if o.is_closed:
            return 'issues.editclosed_issue'

        return 'issues.add_issue' if o.created_by == self.request.user \
            else 'issues.editopen_issue'

    def get_success_url(self):
        return "" if self.issue.active else "-"

    def delete(self, request, *args, **kwargs):
        o = self.get_object()
        o.active = False
        o.save()
        return HttpResponse("-")


class ProposalCreateView(AjaxFormView, IssueMixin, CreateView):
    model = models.Proposal

    def get_required_permission(self):
        return 'issues.editclosedproposal' if self.get_object().is_closed \
            else 'issues.add_proposal'

    form_class = CreateProposalForm

    @property
    def issue(self):
        return get_object_or_404(models.Issue, community=self.community, pk=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super(ProposalCreateView, self).get_context_data(**kwargs)

        context['issue'] = self.issue

        return context

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.issue = self.issue
        return super(ProposalCreateView, self).form_valid(form)

    def get_success_url(self):
        return self.issue.get_absolute_url()

    def get_form_kwargs(self):
        d = super(ProposalCreateView, self).get_form_kwargs()
        d['prefix'] = 'proposal'
        return d


class ProposalMixin(IssueMixin):
    model = models.Proposal

    @property
    def issue(self):
        return get_object_or_404(models.Issue, community=self.community,
                                 pk=self.kwargs['issue_id'])

    def get_queryset(self):
        return models.Proposal.objects.filter(issue=self.issue)


class ProposalDetailView(ProposalMixin, DetailView):

    def get_required_permission(self):
        o = self.get_object()
        return 'issues.viewclosed_proposal' if o.issue.is_closed else 'issues.viewopen_proposal'

    def get_required_permission_for_post(self):
        o = self.get_object()
        return 'issues.acceptclosed_proposal' if o.issue.is_closed else 'issues.acceptopen_proposal'

    def post(self, request, *args, **kwargs):
        p = self.get_object()
        p.is_accepted = request.POST['accepted'] == "0"
        p.accepted_at = datetime.datetime.now() if p.is_accepted else None
        p.save()

        return HttpResponse(json.dumps(int(p.is_accepted)),
                             content_type='application/json')


class ProposalEditView(AjaxFormView, ProposalMixin, UpdateView):
    form_class = EditProposalForm

    reload_on_success = True

    def get_required_permission(self):
        o = self.get_object()
        return 'issues.editclosed_proposal' if o.issue.is_closed else 'issues.edittask_proposal'


class ProposalEditTaskView(ProposalMixin, UpdateView):
    form_class = EditProposalTaskForm

    def get_queryset(self):
        return super(ProposalEditTaskView, self).get_queryset().filter(type=ProposalType.TASK)

    def get_required_permission(self):
        o = self.get_object()
        return 'issues.editclosed_proposal' if o.issue.is_closed else 'issues.editopen_proposal'


class ProposalDeleteView(AjaxFormView, ProposalMixin, DeleteView):

    def get_required_permission(self):
        o = self.get_object()
        if o.issue.is_closed:
            return 'issues.editclosed_issue'

        return 'issues.add_proposal' if o.created_by == self.request.user \
            else 'issues.editopen_proposal'

    def get_success_url(self):
        return "" if self.issue.active else "-"

    def delete(self, request, *args, **kwargs):
        o = self.get_object()
        o.active = False
        o.save()
        return HttpResponse("-")
