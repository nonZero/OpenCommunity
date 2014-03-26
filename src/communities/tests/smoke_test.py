from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.test.testcases import TestCase

from users.default_roles import DefaultGroups
from users.models import Membership

PASSWORD = 'secret'

User = get_user_model()

from communities.models import Community


class CommunitiesTest(TestCase):
    @classmethod
    def create_member(cls, username, community=None):
        u = User.objects.create_user(
            '{}@gmail.com'.format(username), username.title(), PASSWORD)
        if community:
            Membership.objects.create(community=community, user=u,
                                      default_group_name=DefaultGroups.MEMBER)
        return u

    @classmethod
    def setUpClass(cls):
        cls.c1 = Community.objects.create(name='Public Community XYZZY',
                                          is_public=True)
        cls.c2 = Community.objects.create(name='Private Community ABCDE',
                                          is_public=False)

        cls.not_a_member = cls.create_member("foo")
        cls.c1member = cls.create_member("bar", cls.c1)
        cls.c2member = cls.create_member("baz", cls.c2)


    def visit(self, url, user=None, success=True):
        client = self.client_class()
        if user:
            client.login(email=user.email, password=PASSWORD)
        response = client.get(url)
        self.assertEqual(response.status_code,
                         200 if success else (403 if user else 302))
        return response

    def visit_home(self, user=None):
        response = self.visit(reverse('home'), user)
        self.assertContains(response, self.c1.name)
        return response

    def visit_community(self, community, *args, **kwargs):
        return self.visit(community.get_absolute_url(), *args, **kwargs)

    def test_homepage_anonymous(self):
        response = self.visit_home()
        self.assertNotContains(response, self.c2.name)

    def test_homepage_member(self):
        response = self.visit_home(self.c2member)
        self.assertContains(response, self.c2.name)

    def test_homepage_not_a_member(self):
        response = self.visit_home(self.not_a_member)
        self.assertNotContains(response, self.c2.name)

    def test_visit_community_public_anonymous(self):
        response = self.visit_community(self.c1)

    def test_visit_community_public_logged_in(self):
        response = self.visit_community(self.c1, self.c2member)

    def test_visit_community_public_member(self):
        response = self.visit_community(self.c1, self.c1member)

    def test_visit_community_private_anonymous(self):
        response = self.visit_community(self.c2, success=False)

    def test_visit_community_private_logged_in(self):
        response = self.visit_community(self.c2, self.c1member, success=False)

    def test_visit_community_private_member(self):
        response = self.visit_community(self.c2, self.c2member)

