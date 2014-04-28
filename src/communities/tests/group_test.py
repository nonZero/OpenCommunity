from communities.models import CommunityGroup, CommunityGroupRole
from django.core.exceptions import ValidationError
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
        g.full_clean()
        g.save()

        with transaction.atomic():
            g = CommunityGroup()
            g.community = self.c1
            g.title = "Group ABC"
            self.assertRaises(ValidationError, g.full_clean)
            self.assertRaises(IntegrityError, g.save)


        g = CommunityGroup()
        g.community = self.c1
        g.title = "Group DEF"
        g.full_clean()
        g.save()

        self.assertEquals(2, CommunityGroup.objects.count())

    def test_create_roles(self):

        g = CommunityGroup()
        g.community = self.c1
        g.title = "Group ABC"
        g.full_clean()
        g.save()

        self.assertEquals(0, CommunityGroupRole.objects.count())

        r1 = CommunityGroupRole()
        r1.group = g
        r1.title = "Role #1"
        r1.code = DefaultRoles.VIEWER
        r1.full_clean()
        r1.save()

        r2 = CommunityGroupRole()
        r2.group = g
        r2.title = "Role #2"
        r2.code = DefaultRoles.MANAGER
        r2.full_clean()
        r2.save()

        self.assertEquals(2, CommunityGroupRole.objects.count())
