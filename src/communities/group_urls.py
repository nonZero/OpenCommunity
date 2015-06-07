from communities import views
from django.conf.urls import url


urlpatterns = [
    url(r'^$', views.GroupListView.as_view(), name='list'),
    url(r'^create/$', views.GroupCreateView.as_view(), name='create'),
    url(r'^(?P<pk>\d+)/$', views.GroupDetailView.as_view(), name='detail'),
    url(r'^(?P<pk>\d+)/edit/$', views.GroupUpdateView.as_view(), name='update'),

]
