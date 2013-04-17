from django.conf.urls import patterns, include, url
from django.contrib import admin
import communities.views

admin.autodiscover()

urlpatterns = patterns('',

    url(r'^$', communities.views.CommunityList.as_view(), name='home'),

    url(r'^(?P<pk>\d+)/', include('communities.urls')),

    url(r'^(?P<community_id>\d+)/', include('communities.urls')),
    url(r'^(?P<community_id>\d+)/issues/', include('issues.urls')),
    url(r'^(?P<community_id>\d+)/history/', include('meetings.urls')),

    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),

)
