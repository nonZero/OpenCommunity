from django.core.management.base import BaseCommand
from communities.emails import mail_upcoming

class Command(BaseCommand):
    args = 'TEST_ARG'
    help = 'Closes the meeting and send mail'

    def handle(self, *args, **options):
       # send_mail('Subject here', 'Here is the message.', 'from@example.com',
       #           ['to@example.com'], fail_silently=False)
        mail_upcoming(self.community)

        self.stdout.write('Successfully sent')
