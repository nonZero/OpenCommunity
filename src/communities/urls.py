from communities import views
from django.conf.urls import patterns, url

urlpatterns = patterns('',

    url(r'^$', views.UpcomingMeetingView.as_view(), name='community'),

    url(r'^upcoming/publish/$', views.PublishUpcomingView.as_view(),
        name="upcoming_publish"),

    url(r'^upcoming/start/$', views.StartMeetingView.as_view(),
        name="upcoming_start"),

    url(r'^upcoming/end/$', views.EndMeetingView.as_view(),
        name="upcoming_end"),

    url(r'^edit-summary/$', views.EditUpcomingSummaryView.as_view(),
        name="upcoming_edit_summary"),

    url(r'^upcoming/publish/preview/$',
        views.PublishUpcomingMeetingPreviewView.as_view(),
        name='preview_upcoming_meeting'),

    url(r'^upcoming/edit/$', views.EditUpcomingMeetingView.as_view(),
        name="upcoming_edit"),

    url(r'^upcoming/participants/$',
        views.EditUpcomingMeetingParticipantsView.as_view(),
        name="upcoming_edit_participants"),

    url(r'^upcoming/participants/delete-participant/(?P<participant_id>\d+)/$', views.DeleteParticipantView.as_view(), 
        name="delete_participant"),

    # FOR TESTING ONLY!
    url(r'^upcoming/sum_votes/$', views.SumVotesView.as_view(), name="sum_votes"),
        
    url(r'^protocol-preview/$',
        views.ProtocolDraftPreviewView.as_view(),
        name='preview_ongoing_protocol'),

    url(r'^assignments/$',
        views.AssignmentsView.as_view(), name="assignments"),

    url(r'^procedures/$',
        views.ProceduresView.as_view(), name="procedures"),

    url(r'^search/$', views.search_view_factory(
          template='communities/community_search.html',
          view_class=views.CommunitySearchView
       ), name='community_search'),

    url(r'^search_procedures/$', views.search_view_factory(
          template='communities/procedure_list.html',
          view_class=views.ProcedureSearchView  
       ), name='procedure_search'),
)
