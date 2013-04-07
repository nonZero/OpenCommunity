from communities import models
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.views.generic import ListView
from django.views.generic.base import RedirectView


class CommunityList(ListView):
    model = models.Community


#class CommunityDetailView(DetailView):
    #model = models.Community

class CommunityDetailView(RedirectView):
    def get_redirect_url(self, **kwargs):
        self.community = get_object_or_404(models.Community, pk = self.kwargs['pk'])
        return reverse('issues', args=(str(self.community.id),))