from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin
from meetings.views import MeetingCreateView
from users.forms import OCPasswordResetForm, OCPasswordResetConfirmForm
from users.models import CODE_LENGTH
from users.views import AcceptInvitationView
import communities.views

admin.autodiscover()

urlpatterns = patterns('',

    url(r'^$', communities.views.CommunityList.as_view(), name='home'),

    url(r'^about/$', communities.views.About.as_view(), name='about'),

    url(r'^(?P<pk>\d+)/', include('communities.urls')),

    url(r'^(?P<community_id>\d+)/upcoming/close/$',
            MeetingCreateView.as_view(),
            name="upcoming_close"),

    url(r'^(?P<community_id>\d+)/members/', include('users.urls')),
    url(r'^(?P<community_id>\d+)/issues/', include('issues.urls')),
    url(r'^(?P<community_id>\d+)/history/', include('meetings.urls')),

    url(r'^login/$', 'ocd.views.login_user', {
                                         'template_name': 'login.html'},
                                                         name="login"),

    url(r'^logout/$', 'django.contrib.auth.views.logout',
            {'next_page': '/'}, name="logout"),

    url(r'^invitation/(?P<code>[a-z0-9]{%d})/$' % CODE_LENGTH,
            AcceptInvitationView.as_view(),
            name="accept_invitation"),

    url(r'^user/password/reset/$',
        'users.views.oc_password_reset',
        {'post_reset_redirect': '/user/password/reset/done/',
         'password_reset_form': OCPasswordResetForm},
        name="password_reset"),
    url(r'^user/password/reset/done/$',
        'django.contrib.auth.views.password_reset_done'),
    url(r'^user/password/reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$',
        'django.contrib.auth.views.password_reset_confirm',
        {'post_reset_redirect': '/user/password/done/',
         'set_password_form': OCPasswordResetConfirmForm}),
    url(r'^user/password/done/$',
        'django.contrib.auth.views.password_reset_complete'),

    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),

    url(r'^jsi18n/$', 'django.views.i18n.javascript_catalog',
        {'packages': ('issues', 'communities',)}, 'jsi18n'),

) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
