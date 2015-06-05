from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.core.urlresolvers import reverse_lazy
from meetings.views import MeetingCreateView
from users.forms import OCPasswordResetForm, OCPasswordResetConfirmForm
from users.models import CODE_LENGTH
from users.views import AcceptInvitationView
import communities.views


urlpatterns = [

    url(r'^$', communities.views.LandingPage.as_view(), name='landing'),

    url(r'^communities/$', communities.views.CommunityList.as_view(), name='home'),

    url(r'^about/$', communities.views.About.as_view(), name='about'),

    url(r'^c/(?P<community_slug>[a-z][a-z0-9-]+)/members/', include('users.urls')),
    url(r'^c/(?P<community_slug>[a-z][a-z0-9-]+)/', include('communities.urls')),

    url(r'^c/(?P<community_slug>[a-z][a-z0-9-]+)/(?P<committee_slug>[a-z][a-z0-9-]+)/upcoming/close/$',
        MeetingCreateView.as_view(),
        name="upcoming_close"),

    url(r'^c/(?P<community_slug>[a-z][a-z0-9-]+)/(?P<committee_slug>[a-z][a-z0-9-]+)/issues/', include('issues.urls')),
    url(r'^c/(?P<community_slug>[a-z][a-z0-9-]+)/(?P<committee_slug>[a-z][a-z0-9-]+)/history/', include('meetings.urls')),

    url(r'^login/$', 'ocd.views.login_user', {'template_name': 'login.html'}, name="login"),

    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': reverse_lazy('home')},
        name="logout"),

    url(r'^invitation/(?P<code>[a-z0-9]{%d})/$' % CODE_LENGTH, AcceptInvitationView.as_view(),
        name="accept_invitation"),

    url(r'^user/password/reset/$', 'users.views.oc_password_reset',
        {'post_reset_redirect': '/user/password/reset/done/', 'password_reset_form': OCPasswordResetForm},
        name="password_reset"),
    url(r'^user/password/reset/done/$', 'django.contrib.auth.views.password_reset_done'),
    url(r'^user/password/reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$',
        'django.contrib.auth.views.password_reset_confirm',
        {'post_reset_redirect': '/user/password/done/', 'set_password_form': OCPasswordResetConfirmForm}),
    url(r'^user/password/done/$', 'django.contrib.auth.views.password_reset_complete'),

    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),

    url(r'^django-rq/', include('django_rq.urls')),

    url(r'^jsi18n/$', 'django.views.i18n.javascript_catalog', {'packages': ('issues', 'communities',)},
        'jsi18n'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
