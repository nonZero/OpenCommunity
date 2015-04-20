from communities.models import Community
from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import TestCase
from issues.models import Issue, Proposal, ProposalType, ProposalVote, ProposalVoteValue, ProposalVoteArgument


User = get_user_model()


class IssuesTest(TestCase):
    def setUp(self):
        self.c = Community.objects.create(name="TEST COMMUNITY")
        self.u = User.objects.create(email="testuser@foo.com")
        self.i = Issue.objects.create(community=self.c, title="Issue ABC",
                       created_by=self.u)
        self.p = Proposal.objects.create(type=ProposalType.RULE,
                                         issue=self.i,
                                         created_by=self.u,
                                         title='Proposal XYZ',
                                         content='hellow world')
        self.pv = ProposalVote.objects.create(proposal=self.p,
                                              user=self.u,
                                              value=ProposalVoteValue.PRO)

    def test_arguments_lists(self):
        self.u2 = User.objects.create(email="testuser2@foo.com")
        self.u3 = User.objects.create(email="testuser3@foo.com")
        self.pv2 = ProposalVote.objects.create(proposal=self.p,
                                              user=self.u2,
                                              value=ProposalVoteValue.PRO)
        self.pv3 = ProposalVote.objects.create(proposal=self.p,
                                              user=self.u3,
                                              value=ProposalVoteValue.CON)

        content = 'My test argument, this proposal is very good'
        self.pva1 = ProposalVoteArgument.objects.create(proposal_vote=self.pv,
                                                        argument=content,
                                                        created_by=self.u)
        self.pva2 = ProposalVoteArgument.objects.create(proposal_vote=self.pv2,
                                                        argument=content,
                                                        created_by=self.u2)
        self.pva3 = ProposalVoteArgument.objects.create(proposal_vote=self.pv3,
                                                        argument=content,
                                                        created_by=self.u3)
        self.assertEquals(set(self.p.arguments_for), set([self.pva1, self.pva2]))
        self.assertEquals(set(self.p.arguments_against), set([self.pva3]))
        self.assertEquals(set(self.p.elegantly_interleaved_for_and_against_arguments), set([self.pva1, self.pva2, self.pva3]))

    def test_arguments_lists_only_con(self):
        self.u2 = User.objects.create(email="testuser2@foo.com")
        self.u3 = User.objects.create(email="testuser3@foo.com")
        self.pv2 = ProposalVote.objects.create(proposal=self.p,
                                              user=self.u2,
                                              value=ProposalVoteValue.PRO)
        self.pv3 = ProposalVote.objects.create(proposal=self.p,
                                              user=self.u3,
                                              value=ProposalVoteValue.CON)

        content = 'My test argument, this proposal is very good'
        self.pva3 = ProposalVoteArgument.objects.create(proposal_vote=self.pv3,
                                                        argument=content,
                                                        created_by=self.u3)
        self.assertEquals(set(self.p.arguments_against), set([self.pva3]))
        self.assertEquals(set(self.p.elegantly_interleaved_for_and_against_arguments), set([self.pva3]))
