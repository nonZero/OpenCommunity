from communities.models import Community
from django.core import mail
from django.test import TestCase
from users import models
from users.models import OCUser


class UsersModelsTest(TestCase):

    def test_send_invitation(self):

        c = Community.objects.create(name="Foo Inc.")
        u = OCUser.objects.create_user("foo@foo.inc", "Foo Bar")
        i = models.Invitation.objects.create(community=c, created_by=u)
        i.send()

        self.assertEqual(len(mail.outbox), 1)

        print mail.outbox[0].message()

        self.assertEqual(mail.outbox[0].subject, 'FAILME')
