from django.db import models
from django.db.models.query import QuerySet
from haystack.query import SearchQuerySet
from users.default_roles import DefaultGroups


class ActiveQuerySetMixin(object):

    """Exposes methods that can be used on both the manager and the queryset.

    This allows us to chain custom methods.

    """

    def active(self):
        return self.get_queryset().filter(active=True)


class ConfidentialQuerySetMixin(object):

    """Exposes methods that can be used on both the manager and the queryset.

    This allows us to chain custom methods.

    """

    def object_access_control(self, user=None, community=None):

        if not user or not community:
            raise ValueError('The object access control method requires '
                             'both a user and a community object.')

        if hasattr(user, '_is_mock') and user._is_mock is True:
            return self.filter(is_confidential=False)

        elif user.is_superuser:
            return self.all()

        elif user.is_anonymous():
            return self.filter(is_confidential=False)

        else:
            # we have a membership. return according to member's level.
            # TODO: hook properly into permission system.
            memberships = user.memberships.filter(community=community)
            lookup = [m.default_group_name for m in memberships]
            if DefaultGroups.MEMBER in lookup and len(lookup) == 1:
                return self.filter(is_confidential=False)
            else:
                return self.all()


class ConfidentialQuerySet(QuerySet, ConfidentialQuerySetMixin):
    pass


class ConfidentialManager(models.Manager, ConfidentialQuerySetMixin):

    def get_queryset(self):
        return ConfidentialQuerySet(self.model, using=self._db)


class ConfidentialSearchQuerySet(SearchQuerySet):

    def object_access_control(self, user=None, community=None, **kwargs):
        if not user or not community:
            raise ValueError('The access validator requires both a user and '
                             'a community object.')
        qs = self._clone()
        if user.is_superuser:
            return qs
        elif user.is_anonymous():
            return qs.filter(is_confidential=False)
        else:
            memberships = user.memberships.filter(community=community)
            lookup = [m.default_group_name for m in memberships]
            if DefaultGroups.MEMBER in lookup and len(lookup) == 1:
                return qs.filter(is_confidential=False)
        return qs
