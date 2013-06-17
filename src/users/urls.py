from django.conf.urls import patterns, url
from users import views


urlpatterns = patterns('',

    url(r'^$', views.MembershipList.as_view(), name="members"),
    url(r'^(?P<pk>\d+)/delete-invitation/$', views.DeleteInvitationView.as_view(), 
        name="delete_invitation"),

)
