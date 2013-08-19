from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin
from meetings.views import MeetingCreateView
from users.models import CODE_LENGTH
from users.views import AcceptInvitationView
import communities.views

admin.autodiscover()

urlpatterns = patterns('',

    url(r'^$', communities.views.CommunityList.as_view(), name='home'),

    url(r'^(?P<pk>\d+)/', include('communities.urls')),

    url(r'^(?P<community_id>\d+)/upcoming/close/$',
            MeetingCreateView.as_view(),
            name="upcoming_close"),

    url(r'^(?P<community_id>\d+)/members/', include('users.urls')),
    url(r'^(?P<community_id>\d+)/issues/', include('issues.urls')),
    url(r'^(?P<community_id>\d+)/history/', include('meetings.urls')),

    url(r'^login/$', 'django.contrib.auth.views.login', {
                                         'template_name': 'login.html'},
                                                         name="login"),

    url(r'^logout/$', 'django.contrib.auth.views.logout',
            {'next_page': '/'}, name="logout"),

    url(r'^invitation/(?P<code>[a-z0-9]{%d})/$' % CODE_LENGTH,
            AcceptInvitationView.as_view(),
            name="accept_invitation"),



    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),

) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
