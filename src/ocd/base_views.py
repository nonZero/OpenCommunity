from communities.models import Community
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponseForbidden
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator


class LoginRequiredMixin(object):

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(request, *args, **kwargs)


class ProtectedMixin(object):

    required_permission = None
    required_permission_for_post = None

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):

        if hasattr(self, 'get_required_permission'):
            perm = self.get_required_permission()
        else:
            perm = self.required_permission or "communities.access_community"

        if not request.user.has_community_perm(self.community, perm):
            if settings.DEBUG:
                return HttpResponseForbidden("403 %s" % perm)
            return HttpResponseForbidden("403 Unauthorized")

        if request.method == "POST":
            if hasattr(self, 'get_required_permission_for_post'):
                perm = self.get_required_permission_for_post()
            else:
                perm = self.required_permission_for_post or "communities.access_community"

            if not request.user.has_community_perm(self.community, perm):
                if settings.DEBUG:
                    return HttpResponseForbidden("403 POST %s" % perm)
                return HttpResponseForbidden("403 Unauthorized")

        return super(ProtectedMixin, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        d = super(ProtectedMixin, self).get_context_data(**kwargs)
        d['cperms'] = self.request.user.get_community_perms(self.community)
        return d


class CommunityMixin(ProtectedMixin):

    _community = None

    @property
    def community(self):
        if not self._community:
            self._community = get_object_or_404(Community, pk=self.kwargs['community_id'])
        return self._community

