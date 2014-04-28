from django.test import TestCase
from acl.default_roles import DefaultGroups
from communities.tests.common import create_community


class BoardTest(TestCase):
    def setUp(self):
        roles = (
            [DefaultGroups.CHAIRMAN] +
            [DefaultGroups.SECRETARY] * 2 +
            [DefaultGroups.BOARD] * 5 +
            [DefaultGroups.MEMBER] * 10)

        (self.c, self.members, self.chairmen) = create_community(roles)

        roles2 = (
            [DefaultGroups.CHAIRMAN] * 3 +
            [DefaultGroups.SECRETARY] * 4 +
            [DefaultGroups.BOARD] * 6 +
            [DefaultGroups.MEMBER] * 8)

        (self.c2, self.members2, self.chairmen2) = create_community(roles2, community_name="Bar Inc.")


    def test_board(self):
        self.assertEquals(18, self.c.memberships.count())
        self.assertEquals(8, self.c.memberships.board().count())

        self.assertEquals(21, self.c2.memberships.count())
        self.assertEquals(13, self.c2.memberships.board().count())
