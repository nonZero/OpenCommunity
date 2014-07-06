import datetime
from django.contrib.auth import get_user_model
from django.test import TestCase
from communities.models import Community
from users.models import DefaultGroups, Membership
from meetings.models import Meeting
from issues.models import (Issue, IssueComment, IssueCommentRevision,
                           IssueAttachment, Proposal, ProposalVote,
                           ProposalVoteBoard, VoteResult)


User = get_user_model()


class ConfidentialLogicTestCase(TestCase):

    """Tests the logic setting `access` and `confidential` properties."""

    def setUp(self):
        self.community = Community.objects.create(name="A Community")
        self.user_pool = {}
        self.issue_pool = {}

        for group_type, group_name in DefaultGroups.CHOICES:
            user = User.objects.create(
                email='user+' + group_type + '@email.com')
            Membership.objects.create(user=user, community=self.community,
                                      default_group_name=group_type)

            self.user_pool.update({group_type: user})

        self.meeting = Meeting.objects.create(community=self.community,
                                              title="A Meeting",
                                              created_by=self.user_pool['chairman'],
                                              held_at=datetime.date(2014, 01, 01))

        for reason in self.community.confidential_reasons.all():
            instances = {}
            instances['issue'] = Issue.objects.create(community=self.community,
                                                      created_by=self.user_pool['chairman'],
                                                      title=reason,
                                                      abstract=reason,
                                                      confidential_reason=reason)
            instances['comment'] = IssueComment.objects.create(
                issue=instances['issue'], meeting=self.meeting,
                content=reason, created_by=self.user_pool['chairman'])
            instances['comment_revision'] = IssueCommentRevision.objects.create(
                comment=instances['comment'], version=1, content=reason,
                created_by=self.user_pool['chairman'])
            instances['attachment'] = IssueAttachment.objects.create(
                issue=instances['issue'], file='/some/path.jpg',
                title=reason, created_by=self.user_pool['chairman'])
            instances['proposal'] = Proposal.objects.create(
                issue=instances['issue'], title=reason,
                content=reason, confidential_reason=reason,
                created_by=self.user_pool['chairman'], type=1)

            instances['proposal_vote'] = ProposalVote.objects.create(
                proposal=instances['proposal'], user=self.user_pool['board'],
                value=1)

            instances['proposal_vote_board'] = ProposalVoteBoard.objects.create(
                proposal=instances['proposal'], user=self.user_pool['chairman'],
                value=1, voted_by_chairman=True)

            instances['vote_result'] = VoteResult.objects.create(
                proposal=instances['proposal'], meeting=self.meeting,
                votes_pro=3, votes_con=7, community_members=10)

            self.issue_pool.update({reason.title: instances})

        open_instances = {}
        open_instances['issue'] = Issue.objects.create(community=self.community,
                                                  created_by=self.user_pool['chairman'],
                                                  title='open',
                                                  abstract='open')
        open_instances['comment'] = IssueComment.objects.create(
            issue=open_instances['issue'], meeting=self.meeting,
            content='open', created_by=self.user_pool['chairman'])
        open_instances['comment_revision'] = IssueCommentRevision.objects.create(
            comment=open_instances['comment'], version=1, content='open',
            created_by=self.user_pool['chairman'])
        open_instances['attachment'] = IssueAttachment.objects.create(
            issue=open_instances['issue'], file='/some/path.jpg',
            title='open', created_by=self.user_pool['chairman'])
        open_instances['proposal'] = Proposal.objects.create(
            issue=open_instances['issue'], title='open',
            content='open',
            created_by=self.user_pool['chairman'], type=1)

        open_instances['proposal_vote'] = ProposalVote.objects.create(
            proposal=open_instances['proposal'], user=self.user_pool['board'],
            value=1)

        open_instances['proposal_vote_board'] = ProposalVoteBoard.objects.create(
            proposal=open_instances['proposal'], user=self.user_pool['chairman'],
            value=1, voted_by_chairman=True)

        open_instances['vote_result'] = VoteResult.objects.create(
            proposal=open_instances['proposal'], meeting=self.meeting,
            votes_pro=3, votes_con=7, community_members=10)

        self.issue_pool.update({'open': open_instances})

    def test_issue_confidentiality_based_on_access_field(self):
        for k, v in self.issue_pool.items():
            if k == 'open':
                self.assertFalse(v['issue'].is_confidential)
            else:
                self.assertTrue(v['issue'].is_confidential)

    def test_issue_confidentiality_inherited_by_comments(self):
        for k, v in self.issue_pool.items():
            self.assertEqual(v['issue'].is_confidential,
                             v['comment'].is_confidential)

    def test_issue_confidentiality_inherited_by_comment_revisions(self):
        for k, v in self.issue_pool.items():
            self.assertEqual(v['issue'].is_confidential,
                             v['comment_revision'].is_confidential)

    def test_issue_confidentiality_inherited_by_attachments(self):
        for k, v in self.issue_pool.items():
            self.assertEqual(v['issue'].is_confidential,
                             v['attachment'].is_confidential)

    def test_issue_confidentiality_inherited_by_proposals(self):
        for k, v in self.issue_pool.items():
            if v['proposal'].confidential_reason == 'open':
                self.assertEqual(v['issue'].is_confidential,
                                 v['proposal'].is_confidential)

    def test_issue_confidentiality_inherited_by_proposal_votes(self):
        for k, v in self.issue_pool.items():
            self.assertEqual(v['issue'].is_confidential,
                             v['proposal_vote'].is_confidential)

    def test_issue_confidentiality_inherited_by_proposal_board_votes(self):
        for k, v in self.issue_pool.items():
            self.assertEqual(v['issue'].is_confidential,
                             v['proposal_vote_board'].is_confidential)

    def test_open_issue_can_have_closed_proposals(self):
        open_set = self.issue_pool.get('open')
        open_set['proposal'].confidential_reason = self.community.confidential_reasons.all()[0]
        open_set['proposal'].save()

        self.assertFalse(open_set['issue'].is_confidential)
        self.assertTrue(open_set['proposal'].is_confidential)

    def test_proposal_confidentiality_inherited_by_proposal_votes_on_open_issue(self):
        open_set = self.issue_pool.get('open')
        open_set['proposal'].confidential_reason = self.community.confidential_reasons.all()[1]
        open_set['proposal'].save()

        self.assertFalse(open_set['issue'].is_confidential)
        self.assertTrue(open_set['proposal'].is_confidential)
        self.assertTrue(open_set['proposal_vote'].is_confidential)

    def test_proposal_confidentiality_inherited_by_proposal_board_votes_on_open_issue(self):
        open_set = self.issue_pool.get('open')
        open_set['proposal'].confidential_reason = self.community.confidential_reasons.all()[1]
        open_set['proposal'].save()

        self.assertFalse(open_set['issue'].is_confidential)
        self.assertTrue(open_set['proposal'].is_confidential)
        self.assertTrue(open_set['proposal_vote'].is_confidential)
        self.assertTrue(open_set['proposal_vote_board'].is_confidential)

    def test_changing_access_on_issue_flows_to_relations(self):
        open_set = self.issue_pool.get('open')
        self.assertFalse(open_set['issue'].is_confidential)
        self.assertFalse(open_set['comment'].is_confidential)
        self.assertFalse(open_set['comment_revision'].is_confidential)
        self.assertFalse(open_set['attachment'].is_confidential)
        self.assertFalse(open_set['proposal'].is_confidential)
        self.assertFalse(open_set['proposal_vote'].is_confidential)
        self.assertFalse(open_set['proposal_vote_board'].is_confidential)

        open_set['issue'].confidential_reason = self.community.confidential_reasons.all()[1]
        open_set['issue'].save()

        self.assertTrue(open_set['issue'].is_confidential)
        self.assertTrue(open_set['comment'].is_confidential)
        self.assertTrue(open_set['comment_revision'].is_confidential)
        self.assertTrue(open_set['attachment'].is_confidential)
        self.assertTrue(open_set['proposal'].is_confidential)
        self.assertTrue(open_set['proposal_vote'].is_confidential)
        self.assertTrue(open_set['proposal_vote_board'].is_confidential)


class ConfidentialAccessTestCase(TestCase):

    """Tests access via request to objects with the `is_confidential` property."""

    # def test_issue_access_for_each_community_role(self):
    #     pass
