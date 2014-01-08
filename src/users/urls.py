from django.conf.urls import patterns, url
from users import views


urlpatterns = patterns('',

    url(r'^$', views.MembershipList.as_view(), name="members"),
    url(r'^(?P<pk>\d+)/', views.MemberProfile.as_view(), name="member_profile"),
    url(r'^(?P<pk>\d+)/delete-invitation/$', views.DeleteInvitationView.as_view(), 
        name="delete_invitation"),
    url(r'^autocomp/$', views.AutocompleteMemberName.as_view(), name="ac_user"),

)
