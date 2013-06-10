from django.shortcuts import render
from django.views.generic.edit import DeleteView
from django.views.generic.list import ListView
from ocd.base_views import CommunityMixin
from users import models
from users.forms import InvitationForm
from users.models import Invitation
from django.http.response import HttpResponse


class MembershipMixin(CommunityMixin):

    model = models.Membership

    def get_queryset(self):
        return models.Membership.objects.filter(community=self.community)


class MembershipList(MembershipMixin, ListView):

    required_permission = 'community.invite_member'

    def get_context_data(self, **kwargs):
        d = super(MembershipList, self).get_context_data(**kwargs)

        d['invites'] = Invitation.objects.filter(community=self.community)
        d['form'] = InvitationForm()

        return d

    def post(self, request, *args, **kwargs):

        form = InvitationForm(request.POST)

        #TODO: check if user or invitation already exists

        if not form.is_valid():
            assert False

        form.instance.community = self.community
        form.instance.created_by = request.user

        i = form.save()

        # TODO: send mail

        return render(request, 'users/_invitation.html', {'object': i})


class DeleteMembershipView(CommunityMixin, DeleteView):

    required_permission = 'community.invite_member'

    model = models.Invitation

    def get_queryset(self):
        return self.model.objects.filter(community=self.community)

    def get(self, request, *args, **kwargs):
        return HttpResponse("?")

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return HttpResponse("OK")

