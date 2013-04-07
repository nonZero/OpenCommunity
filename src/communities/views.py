from communities import models
from django.views.generic import ListView
from django.views.generic.detail import DetailView
#from django.views.generic.base import RedirectView


class CommunityList(ListView):
    model = models.Community


class CommunityDetailView(DetailView):
    model = models.Community

#class CommunityDetailView(RedirectView):
#    model = models.Community