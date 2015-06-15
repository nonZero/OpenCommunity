from communities import views
from django.conf.urls import url


urlpatterns = [
    url(r'^$', views.GroupRoleListView.as_view(), name='list'),
    url(r'^create/$', views.GroupRoleCreateView.as_view(), name='create'),
    url(r'^(?P<pk>\d+)/$', views.GroupRoleDetailView.as_view(), name='detail'),
    url(r'^(?P<pk>\d+)/edit/$', views.GroupRoleUpdateView.as_view(), name='update'),

]
