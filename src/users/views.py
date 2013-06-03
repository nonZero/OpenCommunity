from django.views.generic.list import ListView
from ocd.base_views import CommunityMixin
from users import models


class MembershipMixin(CommunityMixin):

    model = models.Membership

    def get_queryset(self):
        return models.Membership.objects.filter(community=self.community)


class MembershipList(MembershipMixin, ListView):

    required_permission = 'community.invite_member'
