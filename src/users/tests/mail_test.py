from communities.models import  SendToOption
from django.core import mail
from django.test import TestCase
from users import models
from users.default_roles import DefaultGroups
from users.models import OCUser
from communities.tests.common import createTestCommunity


class MailTest(TestCase):

    def setUp(self):
        roles = (
                 [DefaultGroups.CHAIRMAN] +
                 [DefaultGroups.SECRETARY] * 2 +
                 [DefaultGroups.BOARD] * 5 +
                 [DefaultGroups.MEMBER] * 10)
        
        (self.c,self.members,self.chairmen) = createTestCommunity(roles)

        roles2 = (
                 [DefaultGroups.CHAIRMAN] * 3 +
                 [DefaultGroups.SECRETARY] * 4 +
                 [DefaultGroups.BOARD] * 6 +
                 [DefaultGroups.MEMBER] * 8)
        
        (self.c2,self.members2,self.chairmen) = createTestCommunity(roles2,community_name="Bar Inc.")

    def tearDown(self):
        mail.outbox = []

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

