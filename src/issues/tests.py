from communities.models import Community
from django.test import TestCase
from issues.models import Issue
from django.conf import settings
from django.contrib.auth.models import User as UM


class IssuesTest(TestCase):

    def setUp(self):
        self.c = Community.objects.create(name="TEST COMMUNITY")
        self.u = UM.objects.create(username="test_user")

    def test_new_issue(self):
        i = Issue.objects.create(community=self.c,
                                 title="Test",
                                 created_by=self.u)

        c = i.comments.create(content="foo", created_by=self.u)

        self.assertEqual(i, c.issue)
        self.assertEqual(0, len(c.revisions.all()))

        self.assertTrue(c.update_content(1, self.u, "bar"))
        self.assertEqual(2, c.version)
        self.assertEqual(1, len(c.revisions.all()))

        self.assertFalse(c.update_content(1, self.u, "baz"))

        self.assertTrue(c.update_content(2, self.u, "bar"))
        self.assertEqual(2, c.version)
        self.assertEqual(1, len(c.revisions.all()))

        self.assertTrue(c.update_content(2, self.u, "baz"))
        self.assertEqual(3, c.version)
        self.assertEqual(2, len(c.revisions.all()))
