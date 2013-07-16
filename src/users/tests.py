from communities.models import Community, SendToOption
from django.core import mail
from django.test import TestCase
from users import models
from users.default_roles import DefaultGroups
from users.models import OCUser, Membership


class UsersModelsTest(TestCase):

    def setUp(self):
        self.c = Community.objects.create(name="Foo Inc.")

        self.members = []

        roles = (
                 [DefaultGroups.CHAIRMAN] +
                 [DefaultGroups.SECRETARY] * 2 +
                 [DefaultGroups.BOARD] * 5 +
                 [DefaultGroups.MEMBER] * 10)
        for i, g in enumerate(roles):
            u = OCUser.objects.create_user("foo%d@foo.inc" % i,
                                           "Foo Foo %d" % i)
            Membership.objects.create(user=u, community=self.c, default_group_name=g)
            self.members.append(u)

        self.c2 = Community.objects.create(name="Bar Inc.")

        self.members2 = []

        roles2 = (
                 [DefaultGroups.CHAIRMAN] * 3 +
                 [DefaultGroups.SECRETARY] * 4 +
                 [DefaultGroups.BOARD] * 6 +
                 [DefaultGroups.MEMBER] * 8)
        for i, g in enumerate(roles2):
            u = OCUser.objects.create_user("bar%d@bar.inc" % i,
                                           "Bar Bar %d" % i)
            Membership.objects.create(user=u, community=self.c2, default_group_name=g)
            self.members2.append(u)

    def tearDown(self):
        Community.objects.all().delete()
        OCUser.objects.all().delete()
        self.assertEquals(0, Membership.objects.count())
        mail.outbox = []

    def test_board(self):

        self.assertEquals(18, self.c.memberships.count())
        self.assertEquals(8, self.c.memberships.board().count())

        self.assertEquals(21, self.c2.memberships.count())
        self.assertEquals(13, self.c2.memberships.board().count())

    def test_send_agenda(self):
        # template = 'protocol_draft' if c.upcoming_meeting_started else 'agenda'
        template = 'agenda'

        u = self.members[0]
        self.assertEquals(1, self.c.send_mail(template, u, SendToOption.ONLY_ME))
        self.assertEquals(len(mail.outbox), 1)

        mail.outbox = []
        self.assertEquals(8, self.c.send_mail(template, u, SendToOption.BOARD_ONLY))
        self.assertEquals(len(mail.outbox), 8)

        mail.outbox = []
        self.assertEquals(18, self.c.send_mail(template, u, SendToOption.ALL_MEMBERS))
        self.assertEquals(len(mail.outbox), 18)

        u = self.members2[0]

        mail.outbox = []
        self.assertEquals(13, self.c2.send_mail(template, u, SendToOption.BOARD_ONLY))
        self.assertEquals(len(mail.outbox), 13)

        mail.outbox = []
        self.assertEquals(21, self.c2.send_mail(template, u, SendToOption.ALL_MEMBERS))
        self.assertEquals(len(mail.outbox), 21)

        u = OCUser.objects.create_user('baz@baz.com', 'Baz')

        mail.outbox = []
        self.assertEquals(1, self.c.send_mail(template, u, SendToOption.ONLY_ME))
        self.assertEquals(len(mail.outbox), 1)

        mail.outbox = []
        self.assertEquals(9, self.c.send_mail(template, u, SendToOption.BOARD_ONLY))
        self.assertEquals(len(mail.outbox), 9)

        mail.outbox = []
        self.assertEquals(19, self.c.send_mail(template, u, SendToOption.ALL_MEMBERS))
        self.assertEquals(len(mail.outbox), 19)

    def test_send_invitation(self):

        i = models.Invitation.objects.create(community=self.c,
                                             created_by=self.members[0],
                                             email="xxx@xyz.com")
        i.send()

        self.assertEqual(len(mail.outbox), 1)
        self.assertIn(self.c.name, mail.outbox[0].subject)
