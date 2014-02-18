import logging
from communities.tests.common import create_sample_community
from django.contrib.auth import get_user_model

from django.core.urlresolvers import reverse
from django.test.client import Client
from django.test.testcases import TestCase
from users.default_roles import DefaultGroups
from users.models import Membership

User = get_user_model()


class IssuesUITest(TestCase):
    def setUp(self):
        self.community, self.members, self.chairmen = create_sample_community()

        self.client = Client()


    def tearDown(self):
        pass

    def login_chairmen(self):
        self.client.login(username=self.chairmen[0].email, password="password")


    def test_view_create_issue_unauthorized(self):
        self.client.login(email=self.members[-1].email, password='password')
        response = self.client.get(reverse('issue_create', args=(self.community.id,)))
        self.assertEquals(403, response.status_code)

    def test_view_create_issue(self):
        self.login_chairmen()
        response = self.client.get(reverse('issue_create', args=(self.community.id,)))
        self.assertEquals(200, response.status_code)

