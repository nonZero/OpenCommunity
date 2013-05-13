from communities import views
from django.conf.urls import patterns, url

urlpatterns = patterns('',

    url(r'^$', views.CommunityDetailView.as_view(), name='community'),

    url(r'^upcoming/$', views.UpcomingMeetingView.as_view(),
        name='upcoming_meeting'),

    url(r'^upcoming/publish/$', views.PublishUpcomingView.as_view(),
        name="upcoming_publish"),

    url(r'^upcoming/edit/$', views.EditUpcomingMeetingView.as_view(),
        name="upcoming_edit"),

    url(r'^ongoing/$', views.OngoingMeetingView.as_view(),
        name='ongoing_meeting'),


)
