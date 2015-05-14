from django.contrib.auth import views as auth_views
from django.conf import settings


def login_user(request, template_name='registration/login.html', extra_context=None):
    response = auth_views.login(request, template_name, extra_context={'version': settings.OPENCOMMUNITY_VERSION, })
    if request.POST.has_key('remember_me'):
        request.session.set_expiry(settings.SESSION_REMEMBER_DAYS * 24 * 3600)
    return response
