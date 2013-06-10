from django.conf.urls import patterns, include, url
from django.contrib import admin
from meetings.views import MeetingCreateView
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

    url(r'^logout/$', 'django.contrib.auth.views.logout_then_login',
                                name="logout"),

    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'', include('social_auth.urls')),

)
