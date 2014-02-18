from users.models import OCUser, Membership
from communities.models import Community
from collections import namedtuple
from users.default_roles import DefaultGroups


def create_community(roles, community_name="Foo Inc.", email_template=None):
    community = Community.objects.create(name="Foo Inc.")
    members = []
    chairmen = []
    if not email_template:
        words = community_name.lower().split(" ,-_.")
        email_template = words[0] + "%d@" + ".".join(words)
    for i, g in enumerate(roles):
        u = OCUser.objects.create_user(email_template % i,
                                       "%s %d" % (community_name, i), password="password")
        Membership.objects.create(user=u, community=community, default_group_name=g)
        if g == DefaultGroups.CHAIRMAN:
            chairmen.append(u)
        members.append(u)
    return namedtuple('Result', ['community', 'members', 'chairmen'])(community, members, chairmen)


def create_sample_community():
    return create_community(roles=(
        [DefaultGroups.CHAIRMAN] +
        [DefaultGroups.SECRETARY] * 2 +
        [DefaultGroups.BOARD] * 5 +
        [DefaultGroups.MEMBER] * 10))