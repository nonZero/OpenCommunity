from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.test.testcases import TestCase

from users.default_roles import DefaultGroups
from users.models import Membership

PASSWORD = 'secret'

User = get_user_model()

from communities.models import Community


class CommunitiesTest(TestCase):
    def setUp(self):
        self.c1 = Community.objects.create(name='Public Community XYZZY',
                                           is_public=True)
        self.c2 = Community.objects.create(name='Private Community ABCDE',
                                           is_public=False)
        self.assertEquals(2, Community.objects.count())

        self.not_a_member = User.objects.create_user(
            'foo@gmail.com', 'Foo', PASSWORD)
        self.c2member = User.objects.create_user(
            'bar@gmail.com', 'Bar', PASSWORD)

        Membership.objects.create(community=self.c2, user=self.c2member,
                                  default_group_name=DefaultGroups.MEMBER)


    def visit_home(self, user=None):
        if user:
            self.client.login(email=user.email, password=PASSWORD)
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.c1.name)
        return response

    def test_homepage_annonymous(self):
        response = self.visit_home()
        self.assertNotContains(response, self.c2.name)

    def test_homepage_member(self):
        response = self.visit_home(self.c2member)
        self.assertContains(response, self.c2.name)

    def test_homepage_not_a_member(self):
        response = self.visit_home(self.not_a_member)
        self.assertNotContains(response, self.c2.name)
