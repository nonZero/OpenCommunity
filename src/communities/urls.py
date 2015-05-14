from django.conf.urls import url
from . import views


urlpatterns = [

    url(r'^$', views.CommunityDetailView.as_view(), name='community'),

    url(r'^(?P<committee_slug>[a-z0-9_.-]+)/$', views.UpcomingMeetingView.as_view(), name='committee'),

    url(r'^(?P<committee_slug>[a-z0-9_.-]+)/upcoming/publish/$', views.PublishUpcomingView.as_view(),
        name="upcoming_publish"),

    url(r'^(?P<committee_slug>[a-z0-9_.-]+)/upcoming/start/$', views.StartMeetingView.as_view(),
        name="upcoming_start"),

    url(r'^(?P<committee_slug>[a-z0-9_.-]+)/upcoming/end/$', views.EndMeetingView.as_view(),
        name="upcoming_end"),

    url(r'^(?P<committee_slug>[a-z0-9_.-]+)/edit-summary/$', views.EditUpcomingSummaryView.as_view(),
        name="upcoming_edit_summary"),

    url(r'^(?P<committee_slug>[a-z0-9_.-]+)/upcoming/publish/preview/$',
        views.PublishUpcomingMeetingPreviewView.as_view(),
        name='preview_upcoming_meeting'),

    url(r'^(?P<committee_slug>[a-z0-9_.-]+)/upcoming/edit/$', views.EditUpcomingMeetingView.as_view(),
        name="upcoming_edit"),

    url(r'^(?P<committee_slug>[a-z0-9_.-]+)/upcoming/participants/$',
        views.EditUpcomingMeetingParticipantsView.as_view(),
        name="upcoming_edit_participants"),

    url(r'^(?P<committee_slug>[a-z0-9_.-]+)/upcoming/participants/delete-participant/(?P<participant_id>\d+)/$',
        views.DeleteParticipantView.as_view(),
        name="delete_participant"),

    # FOR TESTING ONLY!
    url(r'^(?P<committee_slug>[a-z0-9_.-]+)/upcoming/sum_votes/$', views.SumVotesView.as_view(),
        name="sum_votes"),

    url(r'^(?P<committee_slug>[a-z0-9_.-]+)/protocol-preview/$',
        views.ProtocolDraftPreviewView.as_view(),
        name='preview_ongoing_protocol'),

    url(r'^search/$', views.CommunitySearchView.as_view(), name='community_search'),

]
