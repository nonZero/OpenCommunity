from django.core.mail import send_mail
from django.template import loader, Context



def mail_upcoming(community):
    # plaintext = get_template('email.txt')
    # htmly     = get_template('upcoming_mail.html')
    #
    # d = Context({ 'community.id': community.id })
    #
    # subject, from_email, to = 'TEST', 'from@example.com', 'to@example.com'
    # text_content = plaintext.render(d)
    # html_content = htmly.render(d)
    # msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    # msg.attach_alternative(html_content, "text/html")
    # msg.send()

    t = loader.get_template('upcoming_mail.html')
    c = Context({
        'object.upcoming_meeting_published_at': community.upcoming_meeting_published_at,
        'product_name': 'Your Product Name',
        'product_url': 'http://www.yourproject.com/',
        'login_url': 'http://www.yourproject.com/login/',
        'username': 'tester0',
    })

    send_mail('Yo', t.render(c), 'from@address.com', 'to@me.com', fail_silently=False)
