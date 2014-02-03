import logging

from django.core.urlresolvers import reverse
from django.test.client import Client
from django.test.testcases import TestCase

from communities.models import Community


class Test(TestCase):


    def setUp(self):
        self.c1 = Community.objects.create(name='my_public_community', is_public=True)
        self.c2 = Community.objects.create(name='my_private_community', is_public=False)
        
        self.client = Client()


    def tearDown(self):
        pass


    def test_homepage(self):
        self.assertEquals(2, Community.objects.count())
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'my_public_community')
        self.assertNotContains(response, 'my_private_community')

