from acl.models import Role
from communities.models import CommunityGroup
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.db import transaction
from django.db.utils import IntegrityError
from django.test.testcases import TestCase

from communities.tests.common import CommunitiesTestMixin
from acl.default_roles import DefaultRoles


class CommunityGroupsTest(CommunitiesTestMixin, TestCase):
    def test_create_group(self):

        self.assertEquals(0, CommunityGroup.objects.count())

        g = CommunityGroup()
        g.community = self.c1
        g.title = "Group ABC"
        g.role = self.r1
        g.full_clean()
        g.save()

        with transaction.atomic():
            g = CommunityGroup()
            g.community = self.c1
            g.title = "Group ABC"
            g.role = self.r1
            self.assertRaises(ValidationError, g.full_clean)
            self.assertRaises(IntegrityError, g.save)


        g = CommunityGroup()
        g.community = self.c1
        g.title = "Group DEF"
        g.role = self.r1
        g.full_clean()
        g.save()

        self.assertEquals(2, CommunityGroup.objects.count())

    def test_visit_groups(self):
        response = self.visit(reverse('groups', args=(self.c1.id,)))
        # self.assertContains(response, self.c1.name)
        # return response
    #
    # def visit_community(self, community, *args, **kwargs):
    #     return self.visit(community.get_absolute_url(), *args, **kwargs)
    #
    # def test_homepage_anonymous(self):
    #     response = self.visit_home()
    #     self.assertNotContains(response, self.c2.name)
    #
    # def test_homepage_member(self):
    #     response = self.visit_home(self.c2member)
    #     self.assertContains(response, self.c2.name)


