from . import views
from django.conf.urls import patterns, url, include

urlpatterns = patterns(
    '',

    url('^roles/', include(patterns(
        '',
        url(r'^$', views.RoleListView.as_view(), name="list"),

        url(r'^new/$', views.RoleCreateView.as_view(), name="create"),

        url(r'^(?P<pk>\d+)/$', views.RoleDetailView.as_view(),
            name="view"),

        url(r'^(?P<pk>\d+)/edit/$', views.RoleUpdateView.as_view(),
            name="edit"),

    ), namespace='role')),
)
