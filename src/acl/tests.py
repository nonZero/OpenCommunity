from acl.default_roles import DefaultRoles
from acl.models import Role
from django.test import TestCase


class RoleTest(TestCase):
    def test_create_role(self):
        self.assertEquals(0, Role.objects.count())

        r = Role()
        r.title = "Dictator"
        r.based_on = DefaultRoles.DECIDER
        r.full_clean()
        r.save()

        self.assertEquals(1, Role.objects.count())

        self.assertEquals(set(r.all_perms()),
                          set(DefaultRoles.permissions[DefaultRoles.DECIDER]))

        r.perms.create(code='access_community')
        self.assertEquals(set(r.all_perms()),
                          set(DefaultRoles.permissions[DefaultRoles.DECIDER]))

        r.perms.create(code='editclosed_issue')
        self.assertEquals(set(r.all_perms()),
                          set(DefaultRoles.permissions[
                                  DefaultRoles.DECIDER] + [
                                  'editclosed_issue']))
