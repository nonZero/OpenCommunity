from acl import models
from acl.forms import RoleForm
from django.db import transaction
from django.views.generic import ListView, CreateView, DetailView
from django.views.generic.edit import UpdateView
from ocd.base_views import SuperUserRequiredMixin


class RoleMixin(SuperUserRequiredMixin):
    model = models.Role


class RoleListView(RoleMixin, ListView):
    pass


class RoleDetailView(RoleMixin, DetailView):
    pass


class EditRoleMixin(RoleMixin):
    form_class = RoleForm

    def get_initial(self):
        d = super(EditRoleMixin, self).get_initial()
        d['perms'] = self.get_initial_perms()
        return d

    def form_valid(self, form):
        with transaction.atomic():
            resp = super(EditRoleMixin, self).form_valid(form)
            cur = frozenset(form.initial['perms'])
            new = frozenset(form.cleaned_data['perms'])
            for v in cur - new:
                form.instance.perms.get(code=v).delete()
            for v in new - cur:
                form.instance.perms.create(code=v)
        return resp


class RoleCreateView(EditRoleMixin, CreateView):
    def get_initial_perms(self):
        return []


class RoleUpdateView(EditRoleMixin, UpdateView):
    def get_initial_perms(self):
        return self.get_object().perms.values_list('code', flat=True)
