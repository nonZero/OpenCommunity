from django.conf.urls import patterns, include, url
from django.contrib import admin
import communities.views

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', communities.views.CommunityList.as_view(), name='home'),
    url(r'^(?P<pk>\d+)/$', communities.views.CommunityDetailView.as_view(), name='community'),
    url(r'^(?P<community_id>\d+)/', include('issues.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
