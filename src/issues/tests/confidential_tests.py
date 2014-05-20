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

        for access_type, access_name in Issue.ACCESS_CHOICES:
            instances = {}
            instances['issue'] = Issue.objects.create(community=self.community,
                                                      created_by=self.user_pool['chairman'],
                                                      title=access_type,
                                                      abstract=access_type,
                                                      access=access_type)
            instances['comment'] = IssueComment.objects.create(
                issue=instances['issue'], meeting=self.meeting,
                content=access_type, created_by=self.user_pool['chairman'])
            instances['comment_revision'] = IssueCommentRevision.objects.create(
                comment=instances['comment'], version=1, content=access_type,
                created_by=self.user_pool['chairman'])
            instances['attachment'] = IssueAttachment.objects.create(
                issue=instances['issue'], file='/some/path.jpg',
                title=access_type, created_by=self.user_pool['chairman'])
            instances['proposal'] = Proposal.objects.create(
                issue=instances['issue'], title=access_type,
                content=access_type, access=access_type,
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

            self.issue_pool.update({access_type: instances})

    def test_issue_confidentiality_based_on_access_field(self):
        for k, v in self.issue_pool.items():
            if k == Issue.ACCESS_OPEN:
                self.assertFalse(v['issue'].confidential)
            else:
                self.assertTrue(v['issue'].confidential)

    def test_issue_confidentiality_inherited_by_comments(self):
        for k, v in self.issue_pool.items():
            self.assertEqual(v['issue'].confidential,
                             v['comment'].confidential)

    def test_issue_confidentiality_inherited_by_comment_revisions(self):
        for k, v in self.issue_pool.items():
            self.assertEqual(v['issue'].confidential,
                             v['comment_revision'].confidential)

    def test_issue_confidentiality_inherited_by_attachments(self):
        for k, v in self.issue_pool.items():
            self.assertEqual(v['issue'].confidential,
                             v['attachment'].confidential)

    def test_issue_confidentiality_inherited_by_proposals(self):
        for k, v in self.issue_pool.items():
            if v['proposal'].access == Issue.ACCESS_OPEN:
                self.assertEqual(v['issue'].confidential,
                                 v['proposal'].confidential)

    def test_issue_confidentiality_inherited_by_proposal_votes(self):
        for k, v in self.issue_pool.items():
            self.assertEqual(v['issue'].confidential,
                             v['proposal_vote'].confidential)

    def test_issue_confidentiality_inherited_by_proposal_board_votes(self):
        for k, v in self.issue_pool.items():
            self.assertEqual(v['issue'].confidential,
                             v['proposal_vote_board'].confidential)

    def test_open_issue_can_have_closed_proposals(self):
        open_set = self.issue_pool.get(Issue.ACCESS_OPEN)
        open_set['proposal'].access = Issue.ACCESS_CHOICES[1][0]
        open_set['proposal'].save()

        self.assertFalse(open_set['issue'].confidential)
        self.assertTrue(open_set['proposal'].confidential)

    def test_proposal_confidentiality_inherited_by_proposal_votes_on_open_issue(self):
        open_set = self.issue_pool.get(Issue.ACCESS_OPEN)
        open_set['proposal'].access = Issue.ACCESS_CHOICES[1][0]
        open_set['proposal'].save()

        self.assertFalse(open_set['issue'].confidential)
        self.assertTrue(open_set['proposal'].confidential)
        self.assertTrue(open_set['proposal_vote'].confidential)

    def test_proposal_confidentiality_inherited_by_proposal_board_votes_on_open_issue(self):
        open_set = self.issue_pool.get(Issue.ACCESS_OPEN)
        open_set['proposal'].access = Issue.ACCESS_CHOICES[1][0]
        open_set['proposal'].save()

        self.assertFalse(open_set['issue'].confidential)
        self.assertTrue(open_set['proposal'].confidential)
        self.assertTrue(open_set['proposal_vote'].confidential)
        self.assertTrue(open_set['proposal_vote_board'].confidential)

    def test_changing_access_on_issue_flows_to_relations(self):
        open_set = self.issue_pool.get(Issue.ACCESS_OPEN)
        self.assertFalse(open_set['issue'].confidential)
        self.assertFalse(open_set['comment'].confidential)
        self.assertFalse(open_set['comment_revision'].confidential)
        self.assertFalse(open_set['attachment'].confidential)
        self.assertFalse(open_set['proposal'].confidential)
        self.assertFalse(open_set['proposal_vote'].confidential)
        self.assertFalse(open_set['proposal_vote_board'].confidential)

        open_set['issue'].access = Issue.ACCESS_CHOICES[1][0]
        open_set['issue'].save()

        self.assertTrue(open_set['issue'].confidential)
        self.assertTrue(open_set['comment'].confidential)
        self.assertTrue(open_set['comment_revision'].confidential)
        self.assertTrue(open_set['attachment'].confidential)
        self.assertTrue(open_set['proposal'].confidential)
        self.assertTrue(open_set['proposal_vote'].confidential)
        self.assertTrue(open_set['proposal_vote_board'].confidential)


class ConfidentialAccessTestCase(TestCase):

    """Tests access via request to objects with the `confidential` property."""

    # def test_issue_access_for_each_community_role(self):
    #     pass
