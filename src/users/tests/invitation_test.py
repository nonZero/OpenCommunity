from django.core import mail
from django.test import TestCase
from users.default_roles import DefaultGroups
from users.models import Invitation, Membership, OCUser
from communities.tests.common import create_sample_community
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext  as _


class InvitationTest(TestCase):
    def setUp(self):
        (self.community, self.members, self.chairmens) = create_sample_community()

    def tearDown(self):
        mail.outbox = []

    def test_send_invitation(self):
        i = Invitation.objects.create(community=self.community,
                                      created_by=self.members[0],
                                      email="xxx@xyz.com")
        i.send(self.members[0])

        self.assertEqual(len(mail.outbox), 1)
        self.assertIn(self.community.name, mail.outbox[0].subject)
        self.assertIn(i.get_absolute_url(), mail.outbox[0].body)


class InvitationViewTest(TestCase):
    def setUp(self):
        (self.community, self.members, self.chairmen) = create_sample_community()

    def tearDown(self):
        mail.outbox = []

    def post_invite(self, data=None):
        if not data:
            data = {"email": "sample@email.com",
                    "default_group_name": DefaultGroups.MEMBER,
                    "message": "the message"}
        return self.client.post(reverse("members"
            , kwargs={"community_id": self.community.id}),
                                data)

    def login_chairmen(self):
        self.client.login(username=self.chairmen[0].email, password="password")

    def test_view(self):
        self.login_chairmen()
        response = self.post_invite({"email": "sample@email.com",
                                     "default_group_name": DefaultGroups.MEMBER,
                                     "message": "the message"})
        self.assertEqual(Invitation.objects.all().count(), 1)
        invitation = Invitation.objects.all()[0]
        self.assertEqual(invitation.community, self.community)
        self.assertEqual(invitation.created_by, self.chairmen[0])
        self.assertEqual(invitation.message, "the message")

        self.assertEqual(len(mail.outbox), 1)

        self.assertEqual(response.status_code, 200)
        #the response is an ajax response the show the user as added
        #to the list of members
        self.assertIn("delete-invitation", response.content)
        self.assertIn("sample@email.com", response.content)


    def test_no_invite_permission(self):
        self.client.login(username=self.members[6].email, password="password")
        response = self.post_invite()
        self.assertEqual(response.status_code, 403)
        self.assertEqual(len(mail.outbox), 0)
        self.assertEqual(Invitation.objects.all().count(), 0)

    def test_bad_email(self):
        self.login_chairmen()
        response = self.post_invite({"email": "not a real email",
                                     "default_group_name": DefaultGroups.MEMBER,
                                     "message": "the message"})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(_("Form error. Please supply a valid email."), response.content)

    def test_invitee_already_invited(self):
        Invitation.objects.create(community=self.community,
                                  created_by=self.chairmen[0],
                                  email="sample@email.com")
        self.login_chairmen()
        response = self.post_invite()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(_("This user is already invited to this community."), response.content)

    def test_invitee_already_a_member(self):
        u = OCUser.objects.create_user("sample@email.com",
                                       "sample user", password="password")
        Membership.objects.create(user=u, community=self.community, default_group_name=DefaultGroups.MEMBER)
        self.login_chairmen()

        response = self.post_invite()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(_("This user already a member of this community."), response.content)