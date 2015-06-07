from acl.default_roles import DefaultGroups, ALL_PERMISSIONS
from users.models import Membership
from collections import defaultdict


"""
These functions work with anonymous users as well, and therefore are not a
part of the OCUser model.
"""


def load_community_permissions(user, community):
    if user.is_authenticated():
        try:
            m = user.memberships.get(community=community)
            return m.get_permissions()
        except Membership.DoesNotExist:
            pass

    if community.is_public:
        return DefaultGroups.permissions[DefaultGroups.MEMBER]

    return []


def get_community_permissions(user, community):
    """ returns a cached list of permissions for a community and a user """

    if not hasattr(user, '_community_permissions_cache'):
        user._community_permissions_cache = {}

    if community.id not in user._community_permissions_cache:
        perms = load_community_permissions(user, community)
        user._community_permissions_cache[community.id] = perms

    return user._community_permissions_cache[community.id]


def has_community_perm(user, community, perm):

    if user.is_active and user.is_superuser:
        return True
  
    return perm in get_community_permissions(user, community)


def get_community_perms(user, community):

    if user.is_active and user.is_superuser:
        perms = ALL_PERMISSIONS
    else:
        perms = get_community_permissions(user, community)

    return perms
    # d = defaultdict(dict)
    # for s in perms:
    #     m, p = s.split('.')
    #     d[m][p] = True
    # return d
