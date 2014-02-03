from django.test import TestCase
from users.models import Invitation, OCUser
from communities.tests.common import create_sample_community


class AcceptInvitationViewTest(TestCase):
    def setUp(self):
        (self.community, self.members, self.chairmen) = create_sample_community()
        self.invitation = Invitation.objects.create(community=self.community,
                                                    created_by=self.chairmen[0],
                                                    email="sample@email.com")

    def test_accept_get(self):
        response = self.client.get(self.invitation.get_absolute_url())
        self.assertIn("sample@email.com", response.content)

    def test_accept(self):
        response = self.client.post(self.invitation.get_absolute_url()
            , {
                                        "display_name": "the users name",
                                        "password1": "pass",
                                        "password2": "pass",
                                        "signup": 1
                                    }, follow=False)
        self.assertEqual(response.status_code, 302)
        self.assertIn(self.community.get_absolute_url(), response._headers["location"][1])
        user = OCUser.objects.get(email="sample@email.com")
        self.assertEqual(user.display_name, "the users name")

    def test_no_display_name(self):
        response = self.client.post(self.invitation.get_absolute_url()
            , {
                                        "display_name": "",
                                        "password1": "pass",
                                        "password2": "pass"
                                    })
        self.assertEqual(response.status_code, 200)
        self.assertIn("This field is required", response.content)
        self.assertEqual(OCUser.objects.filter(email="sample@email.com").count(), 0)

    def test_no_password(self):
        response = self.client.post(self.invitation.get_absolute_url()
            , {
                                        "display_name": "zxczxc",
                                        "password1": "",
                                        "password2": ""
                                    })
        self.assertEqual(response.status_code, 200)
        self.assertIn("This field is required", response.content)
        self.assertEqual(OCUser.objects.filter(email="sample@email.com").count(), 0)

    def test_mismatch_password(self):
        response = self.client.post(self.invitation.get_absolute_url()
            , {
                                        "display_name": "zxczxc",
                                        "password1": "zzz",
                                        "password2": "xxx"
                                    })
        self.assertEqual(response.status_code, 200)
        self.assertIn("Passwords don&#39;t match", response.content)
        self.assertEqual(OCUser.objects.filter(email="sample@email.com").count(), 0)