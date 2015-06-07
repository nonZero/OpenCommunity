from acl.default_roles import DefaultGroups, ALL_PERMISSIONS
from users.models import Membership


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


"""
Same functions as above, this time for committee
"""


def load_committee_permissions(user, committee):
    if user.is_authenticated():
        try:
            m = user.memberships.get(community=committee.community, group_role__committee=committee)
            return m.get_committee_group_permissions()
        except Membership.DoesNotExist:
            pass

    if committee.community.is_public:
        return DefaultGroups.permissions[DefaultGroups.MEMBER]

    return []


def get_committee_permissions(user, committee):
    """ returns a cached list of permissions for a committee and a user """

    if not hasattr(user, '_committee_permissions_cache'):
        user._committee_permissions_cache = {}

    if committee.id not in user._committee_permissions_cache:
        perms = load_committee_permissions(user, committee)
        user._committee_permissions_cache[committee.id] = perms

    return user._committee_permissions_cache[committee.id]


def has_committee_perm(user, committee, perm):

    if user.is_active and user.is_superuser:
        return True

    return perm in get_committee_permissions(user, committee)


def get_committee_perms(user, committee):

    if user.is_active and user.is_superuser:
        perms = ALL_PERMISSIONS
    else:
        perms = get_committee_permissions(user, committee)

    return perms
    # d = defaultdict(dict)
    # for s in perms:
    #     m, p = s.split('.')
    #     d[m][p] = True
    # return d
