from acl.default_roles import DefaultGroups, ALL_PERMISSIONS


"""
These functions work with anonymous users as well, and therefore are not a
part of the OCUser model.
"""


def load_community_permissions(user, community, committee=None):
    from users.models import Membership
    if user.is_authenticated():
        try:
            all_perms = set()
            memberships = user.memberships.filter(community=community)
            for m in memberships:
                if committee:
                    perms = m.get_committee_group_permissions(committee)
                else:
                    perms = m.get_permissions(community)
                all_perms.update(perms)
            return all_perms
        except Membership.DoesNotExist:
            pass

    if community.is_public:
        return DefaultGroups.permissions[DefaultGroups.MEMBER]

    return []


def get_community_permissions(user, community, committee=None):
    """ returns a cached list of permissions for a community and a user """

    if not hasattr(user, '_community_permissions_cache'):
        user._community_permissions_cache = {}

    if community.id not in user._community_permissions_cache:
        perms = load_community_permissions(user, community, committee)
        user._community_permissions_cache[community.id] = perms

    return user._community_permissions_cache[community.id]



def get_committee_permissions(user, committee):
    """ returns a cached list of permissions for a community and a user """

    if not hasattr(user, '_committee_permissions_cache'):
        user._committee_permissions_cache = {}

    if committee.id not in user._committee_permissions_cache:
        perms = load_community_permissions(user, committee.community, committee)
        user._committee_permissions_cache[committee.id] = perms

    return user._committee_permissions_cache[committee.id]



###################################

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