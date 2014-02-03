import logging
from django.contrib.auth import get_user_model

from django.core.urlresolvers import reverse
from django.test.client import Client
from django.test.testcases import TestCase
from users.default_roles import DefaultGroups
from users.models import Membership

User = get_user_model()

from communities.models import Community


class Test(TestCase):
    def setUp(self):
        self.c1 = Community.objects.create(name='Public Community XYZZY', is_public=True)
        self.c2 = Community.objects.create(name='Private Community ABCDE', is_public=False)
        self.assertEquals(2, Community.objects.count())

        self.not_a_member = User.objects.create_user('foo@gmail.com', 'Foo', 'secret')
        self.c2member = User.objects.create_user('bar@gmail.com', 'Bar', 'secret')
        Membership.objects.create(community=self.c2, user=self.c2member, default_group_name=DefaultGroups.MEMBER)

        self.client = Client()


    def tearDown(self):
        pass


    def test_homepage_annonymous(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.c1.name)
        self.assertNotContains(response, self.c2.name)

    def test_homepage_member(self):
        self.client.login(email=self.c2member.email, password='secret')
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.c1.name)
        self.assertContains(response, self.c2.name)

    def test_homepage_not_a_member(self):
        self.client.login(email=self.not_a_member.email, password='secret')
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.c1.name)
        self.assertNotContains(response, self.c2.name)

