from django.conf.urls import patterns, url
from issues import views


urlpatterns = patterns('',

    url(r'^$', views.IssueList.as_view(), name="issues"),

    url(r'^create/$', views.IssueCreateView.as_view(), name="issue_create"),

    url(r'^(?P<pk>\d+)/$', views.IssueDetailView.as_view(), name="issue"),

    url(r'^(?P<pk>\d+)/edit/$', views.IssueEditView.as_view(),
                                name="issue_edit"),

    url(r'^(?P<pk>\d+)/delete/$', views.IssueDeleteView.as_view(),
                                name="issue_delete"),

    url(r'^(?P<pk>\d+)/create-proposal/$', views.ProposalCreateView.as_view(),
            name="proposal_create"),

    url(r'^(?P<issue_id>\d+)/(?P<pk>\d+)/$',
        views.ProposalDetailView.as_view(), name="proposal"),

    url(r'^(?P<issue_id>\d+)/(?P<pk>\d+)/edit/$',
        views.ProposalEditView.as_view(), name="proposal_edit"),

    url(r'^(?P<issue_id>\d+)/(?P<pk>\d+)/edit-task/$',
        views.ProposalEditTaskView.as_view(), name="proposal_edit_task"),

    url(r'^delete-comment/(?P<pk>\d+)/$',
        views.IssueCommentDeleteView.as_view(), name="delete_issue_comment"),

    url(r'^edit-comment/(?P<pk>\d+)/$',
        views.IssueCommentEditView.as_view(), name="edit_issue_comment"),

)
