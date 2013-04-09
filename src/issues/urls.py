from django.conf.urls import patterns, url
from issues import views


urlpatterns = patterns('',
    url(r'^issues/$', views.IssueList.as_view(), name="issues" ),
    url(r'^issues/create/$', views.IssueCreateView.as_view(), name="issue_create" ),
    url(r'^issues/(?P<pk>\d+)/$', views.IssueDetailView.as_view(), name="issue" ),
    url(r'^issues/(?P<pk>\d+)/create-proposal/$', views.ProposalCreateView.as_view(), name="proposal_create" ),
)