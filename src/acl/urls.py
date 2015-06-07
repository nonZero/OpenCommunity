from django.conf.urls import url

from . import views

urlpatterns = [

    url(r'^$', views.RoleListView.as_view(), name="list"),
    url(r'^new/$', views.RoleCreateView.as_view(), name="create"),
    url(r'^(?P<pk>\d+)/$', views.RoleDetailView.as_view(), name="view"),
    url(r'^(?P<pk>\d+)/edit/$', views.RoleUpdateView.as_view(), name="edit"),
]
