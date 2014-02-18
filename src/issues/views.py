import mimetypes
import json

from django.db.models.aggregates import Max
from django.http.response import HttpResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, render, redirect
from django.template import RequestContext
from django.template.loader import render_to_string
from django.views.generic import ListView
from django.views.generic.base import View
from django.views.generic.detail import DetailView, SingleObjectMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from issues import models, forms
from issues.forms import CreateIssueForm, CreateProposalForm, EditProposalForm, \
    UpdateIssueForm, EditProposalTaskForm, AddAttachmentForm, \
    UpdateIssueAbstractForm
from issues.models import ProposalType, Issue, IssueStatus, ProposalVote, \
    ProposalVoteBoard, ProposalVoteValue, VoteResult
from meetings.models import Meeting
from oc_util.templatetags.opencommunity import minutes
from ocd.base_views import CommunityMixin, AjaxFormView, json_response
from ocd.validation import enhance_html
from shultze_vote import send_issue_ranking
from users.default_roles import DefaultGroups
from users.models import Membership


class IssueMixin(CommunityMixin):

    model = models.Issue

    def get_queryset(self):
        return models.Issue.objects.filter(community=self.community,
                                           active=True)


class IssueList(IssueMixin, ListView):

    required_permission = 'issues.viewopen_issue'

    def get_queryset(self):
        return super(IssueList, self).get_queryset().exclude(
              status=IssueStatus.ARCHIVED).order_by('-created_at')

    def get_context_data(self, **kwargs):
        d = super(IssueList, self).get_context_data(**kwargs)
        available_ids = set([x.id for x in self.get_queryset()])
        if d['community'].issue_ranking_enabled:
            d['sorted_issues'] = super(IssueList, self).get_queryset().exclude(
                                    status=IssueStatus.ARCHIVED).order_by('order_by_votes')
            if d['cperms']['issues'].has_key('vote_ranking'):
                my_ranking = models.IssueRankingVote.objects.filter(
                                voted_by=self.request.user,
                                issue__community_id=d['community'].id) \
                                .order_by('rank')
                d['my_vote'] = [i.issue for i in my_ranking if i.issue.active and \
                                                i.issue.status != IssueStatus.ARCHIVED]
                # all_issues_set = set(list(d['sorted_issues']))
                # non_ranked = []
                # list(all_issues_set - set(d['my_vote'])) 
                # for i in self.get_queryset():
                
                d['my_non_ranked'] = [i for i in self.get_queryset() \
                                      if i not in d['my_vote']] 
        return d


    required_permission_for_post = 'issues.vote_ranking'
    
    def post(self, request, *args, **kwargs):
        # TODO: check post permission for user and for each issue
        send_issue_ranking(request)
        return json_response({'res': 'ok', })


class IssueDetailView(IssueMixin, DetailView):

    def get_required_permission(self):
        o = self.get_object()
        return 'issues.viewclosed_issue' if o.is_published else \
            'issues.viewopen_issue'

    def get_context_data(self, **kwargs):
        d = super(IssueDetailView, self).get_context_data(**kwargs)
        m_id = self.request.GET.get('m_id', None)
        d['form'] = forms.CreateIssueCommentForm()
        d['proposal_form'] = forms.CreateProposalForm()
        if m_id:
            d['meeting'] = get_object_or_404(Meeting, id=m_id,
                                            community=self.community)
        else:
            d['meeting'] = None

        if self.request.GET.get('s', None) == '1':
            d['all_issues'] = self.get_queryset().exclude(
                 status=IssueStatus.ARCHIVED).order_by('-created_at')
        return d

    required_permission_for_post = 'issues.add_issuecomment'


    def post(self, request, *args, **kwargs):

        form = forms.CreateIssueCommentForm(request.POST)
        if not form.is_valid():
            return HttpResponseBadRequest()

        i = self.get_object()
        c = i.comments.create(content=enhance_html(form.cleaned_data['content']),
                              created_by=request.user)

        self.object = i  # this makes the next line work
        context = self.get_context_data(object=i, c=c)
        return render(request, 'issues/_comment.html', context)


class IssueCommentMixin(CommunityMixin):
    model = models.IssueComment

    def get_required_permission(self):
        o = self.get_object()
        return 'issues.editopen_issuecomment' if o.issue.is_upcoming else \
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

        context = self.get_context_data(object=c.issue, c=c)
        return render(self.request, 'issues/_comment.html', context)

    def form_invalid(self, form):
        return HttpResponse("")

    def get_form_kwargs(self):
        d = super(IssueCommentEditView, self).get_form_kwargs()
        d['prefix'] = 'ic%d' % self.get_object().id
        return d


class IssueCreateView(AjaxFormView, IssueMixin, CreateView):
    form_class = CreateIssueForm
    template_name = "issues/issue_create_form.html"

    def get_required_permission(self):
        return 'community.editagenda_community' if self.upcoming else 'issues.add_issue'

    upcoming = False

    def form_valid(self, form):
        form.instance.community = self.community
        form.instance.created_by = self.request.user
        form.instance.status = IssueStatus.IN_UPCOMING_MEETING if \
                                     self.upcoming else IssueStatus.OPEN
        if self.upcoming:
            max_upcoming = Issue.objects.filter(
                                community=self.community).aggregate(x=Max(
                                             'order_in_upcoming_meeting'))['x']
            form.instance.order_in_upcoming_meeting = max_upcoming + 1 \
                                                        if max_upcoming else 1

        return super(IssueCreateView, self).form_valid(form)


    def get_success_url(self):
        url = super(IssueCreateView, self).get_success_url()
        if not self.upcoming:
            url += '?s=1'
        return url


class IssueEditView(AjaxFormView, IssueMixin, UpdateView):

    required_permission = 'issues.editopen_issue'

    form_class = UpdateIssueForm

    def form_valid(self, form):
        self.object = form.save()
        return render(self.request, 'issues/_issue_title.html',
                      self.get_context_data())


class IssueEditAbstractView(AjaxFormView, IssueMixin, UpdateView):

    required_permission = 'issues.editopen_issue'

    form_class = UpdateIssueAbstractForm

    def form_valid(self, form):
        self.object = form.save()
        return render(self.request, 'issues/_issue-abstract.html',
                      self.get_context_data())


class IssueCompleteView(IssueMixin, SingleObjectMixin, View):

    required_permission = 'meetings.add_meeting'

    def post(self, request, *args, **kwargs):
        o = self.get_object()
        # TODO: verify that issue is in active meeting
        if request.POST.get('complete') == '1':
            o.completed = True
        elif request.POST.get('undo_complete') == '1':
            o.completed = False
            if o.status == IssueStatus.ARCHIVED:
                o.status = o.statuses.OPEN
        elif request.POST.get('archive') == '1':    
            # TODO: check if issue can be closed 
            o.completed = True
            o.status = IssueStatus.ARCHIVED
        o.save()
        return HttpResponse("-")


class IssueSetLengthView(IssueMixin, SingleObjectMixin, View):

    required_permission = 'community.editagenda_community'

    def post(self, request, *args, **kwargs):
        o = self.get_object()
        s = request.POST.get('length', '').strip()
        if s:
            try:
                l = s.split(':')
                t = int(l[0]) * 60 + int(l[1])
            except:
                return HttpResponseBadRequest("Bad Request")
        else:
            t = None
        o.length_in_minutes = max(min(t, 60 * 24 - 1), 0)
        o.save()
        return HttpResponse(minutes(t) or "--:--")


class IssueDeleteView(AjaxFormView, IssueMixin, DeleteView):

    def get_required_permission(self):
        o = self.get_object()
        if o.is_published:
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


class AttachmentCreateView(AjaxFormView, IssueMixin, CreateView):
    model = models.IssueAttachment
    form_class = AddAttachmentForm

    required_permission = 'issues.editopen_issue'
    reload_on_success = True

    @property
    def issue(self):
        return get_object_or_404(models.Issue, community=self.community, pk=self.kwargs['pk'])

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.issue = self.issue
        return super(AttachmentCreateView, self).form_valid(form)


class AttachmentDeleteView(DeleteView, AjaxFormView):
    model = models.IssueAttachment
    required_permission = 'issues.editopen_issue'

    @property
    def issue(self):
        return get_object_or_404(models.Issue, pk=self.kwargs['issue_id'])

    def delete(self, request, *args, **kwargs):
        o = self.get_object()
        o.file.delete(save=False)
        o.delete()
        return HttpResponse("")


class AttachmentDownloadView(CommunityMixin, SingleObjectMixin, View):

    model = models.IssueAttachment

    def get_required_permission(self):
        o = self.get_object().issue
        return 'issues.viewclosed_issue' if o.is_published else \
            'issues.viewopen_issue'

    def get(self, request, *args, **kwargs):
        o = self.get_object()
        filename = o.file.name.split('/')[-1]
        mime_type = mimetypes.guess_type(filename, True)[0] or "text/plain"
        response = HttpResponse(o.file, content_type=mime_type)
        response['Content-Disposition'] = 'attachment; filename=%s' % filename.encode('utf-8')
        return response


class ProposalCreateView(AjaxFormView, IssueMixin, CreateView):
    model = models.Proposal

    def get_required_permission(self):
        return 'issues.editclosedproposal' if \
            self.get_object().status == IssueStatus.ARCHIVED \
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
        self.object = form.save()
        return render(self.request, 'issues/_proposal.html',
                                  self.get_context_data(proposal=self.object))

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
        return 'issues.viewclosed_proposal' if o.decided_at_meeting else 'issues.viewopen_proposal'

    def get_required_permission_for_post(self):
        o = self.get_object()
        return 'issues.acceptclosed_proposal' if o.decided_at_meeting else 'issues.acceptopen_proposal'
    

    def get_context_data(self, **kwargs):
        """add meeting for the latest straw voting result
           add 'previous_res' var if found previous registered results for this meeting
        """
        context = super(ProposalDetailView, self).get_context_data(**kwargs)
        m_id = self.request.GET.get('m_id', None)
        o = self.get_object()
        
        if m_id:
            context['meeting_context'] = get_object_or_404(Meeting, id=m_id,
                                                    community=self.community)
            participants = context['meeting_context'].participants.all()
        else:
            context['meeting_context'] = None
            participants = o.issue.community.upcoming_meeting_participants.all()

         
        board_votes = ProposalVoteBoard.objects.filter(proposal=o).exclude( \
                                    value=ProposalVoteValue.NEUTRAL)
        try:
            group = self.request.user.memberships.get(community=self.issue.community).default_group_name
        except:
            group = ""

        is_current = o.issue.is_current
        context['res'] = o.get_straw_results()

        results = VoteResult.objects.filter(proposal=o) \
                                    .order_by('-meeting__held_at')

        if o.issue.is_upcoming and \
           self.community.upcoming_meeting_is_published and \
           self.community.straw_vote_ended:
            context['meeting'] = self.community.draft_meeting()
        else:
            if results.count():
                context['meeting'] = results[0].meeting
            else:
                context['meeting'] = None


        show_to_member = group == DefaultGroups.MEMBER and o.decided_at_meeting
        show_to_board = group == DefaultGroups.BOARD and \
                                 (is_current or o.decided_at_meeting)
        show_to_chairman = group == DefaultGroups.CHAIRMAN and o.decided 
        show_board_vote_result = board_votes.count() and \
                                  (show_to_member or show_to_board or show_to_chairman)
        context['issue_frame'] = self.request.GET.get('s', None)
        context['show_board_vote_result'] = show_board_vote_result 
        context['chairman_can_vote'] = is_current and not o.decided
        
        return context

    def post(self, request, *args, **kwargs):
        """ Used to change a proposal status (accept/reject) """
        p = self.get_object()
        v = int(request.POST['accepted'])
        if v not in [
                     p.statuses.ACCEPTED,
                     p.statuses.REJECTED,
                     p.statuses.IN_DISCUSSION
                     ]:
            return HttpResponseBadRequest("Bad value for accepted POST parameter")

        p.status = v
        p.save()

        return redirect(p.issue)


class ProposalEditView(AjaxFormView, ProposalMixin, UpdateView):
    form_class = EditProposalForm

    reload_on_success = True

    def get_required_permission(self):
        o = self.get_object()
        return 'issues.editclosed_proposal' if o.decided_at_meeting else 'issues.edittask_proposal'

    def get_form_kwargs(self):
        d = super(ProposalEditView, self).get_form_kwargs()
        d['prefix'] = 'proposal'
        return d
        
class ProposalEditTaskView(ProposalMixin, UpdateView):
    form_class = EditProposalTaskForm

    def get_queryset(self):
        return super(ProposalEditTaskView, self).get_queryset().filter(type=ProposalType.TASK)

    def get_required_permission(self):
        o = self.get_object()
        return 'issues.editclosed_proposal' if o.decided_at_meeting else 'issues.editopen_proposal'


class ProposalDeleteView(AjaxFormView, ProposalMixin, DeleteView):

    def get_required_permission(self):
        o = self.get_object()
        if o.decided_at_meeting:
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


class VoteResultsView(CommunityMixin, DetailView):
    model = models.Proposal

    def get(self, request, *args, **kwargs):
        meeting = None
        meeting_id = request.GET.get('meeting_id', None)
        p = self.get_object()
        if meeting_id:
            meeting = get_object_or_404(Meeting, id=int(meeting_id))
            res = p.get_straw_results(meeting.id)
        else:
            meeting = self.community.draft_meeting()
            res = p.get_straw_results()

        panel = render_to_string('issues/_proposal_vote_results.html',
                                RequestContext(request, {
                                        'meeting': meeting,
                                        'res': res,
                                        'proposal': p,
                                        }))
        return HttpResponse(panel)


class ProposalVoteView(CommunityMixin, DetailView):
    required_permission_for_post = 'issues.vote'
    model = models.Proposal

    def post(self, request, *args, **kwargs):
        
        if request.POST.get('user'):
            voter_id = request.POST['user']
            vote_class = ProposalVoteBoard
        else:
            voter_id = request.user.id
            vote_class = ProposalVote

        proposal = self.get_object()
        pid = proposal.id

        val = request.POST['val']

        value = ''
        if val == 'pro':
            value = ProposalVoteValue.PRO
        elif val == 'con':
            value = ProposalVoteValue.CON
        elif val == 'reset':
            vote = get_object_or_404(vote_class,
                                     proposal_id=pid, user_id=voter_id)
            vote.delete()
            return json_response({
                'result': 'ok',
                'html': render_to_string('issues/_vote_panel.html',
                                         {
                                             'proposal': proposal,
                                             'community': self.community,
                                         }),
                'sum': render_to_string('issues/_member_vote_sum.html',
                                         {
                                             'proposal': proposal,
                                             'community': self.community,
                                         })
            })

        else:
            return HttpResponseBadRequest('vote value not valid')
        
        vote, created = vote_class.objects.get_or_create(proposal_id=pid, 
                                                         user_id=voter_id)
        vote.value=value
        vote.save()
        return json_response({
            'result': 'ok',
            'html': render_to_string('issues/_vote_reset_panel.html',
                                        {
                                             'proposal': proposal,
                                             'community': self.community,
                                         }),
            'sum': render_to_string('issues/_member_vote_sum.html',
                                     {
                                         'proposal': proposal,
                                         'community': self.community,
                                     })
        })

class MultiProposalVoteView(CommunityMixin, DetailView):
    required_permission_for_post = 'issues.vote'
    model = models.Proposal

    def post(self, request, *args, **kwargs): 
        voter_ids = json.loads(request.POST['users'])
        proposal = self.get_object()
        pid = proposal.id

        val = request.POST['val']

        value = ''
        if val == 'pro':
            value = ProposalVoteValue.PRO
        elif val == 'con':
            value = ProposalVoteValue.CON
        elif val == 'reset':
            ProposalVoteBoard.objects.filter(proposal_id=pid,
                                        user_id__in=voter_ids).delete()
            return json_response({
                'result': 'ok',
                'html': render_to_string('issues/_vote_panel.html',
                                         {
                                             'proposal': proposal,
                                             'community': self.community,
                                         }),
                'sum': render_to_string('issues/_member_vote_sum.html',
                                         {
                                             'proposal': proposal,
                                             'community': self.community,
                                         })
            })

        else:
            return HttpResponseBadRequest('vote value not valid')

        for user_id in voter_ids:
            vote, created = ProposalVoteBoard.objects.get_or_create(
                        proposal_id=pid, user_id=user_id)
            vote.value = value
            vote.save()
        return json_response({
            'result': 'ok',
            'html': render_to_string('issues/_vote_reset_panel.html',
                                        {
                                             'proposal': proposal,
                                             'community': self.community,
                                         }),
            'sum': render_to_string('issues/_member_vote_sum.html',
                                     {
                                         'proposal': proposal,
                                         'community': self.community,
                                     })
        })