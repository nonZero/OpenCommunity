from django.utils.translation import ugettext_lazy as _
import itertools


class DefaultRoles(object):

    VIEWER = 'viewer'
    OBSERVER = 'observer'
    PARTICIPANT = 'participant'
    PROPOSER = 'proposer'
    CONTRIBUTOR = 'contributor'
    EDITOR = 'editor'
    OPERATOR = 'operator'
    DECIDER = 'decider'
    MANAGER = 'manager'

    permissions = {}

    permissions[VIEWER] = [
                           'communities.access_community',
                           'issues.viewclosed_issue',
                           'issues.viewclosed_proposal',
                           'meetings.view_meeting',
                           ]

    permissions[OBSERVER] = permissions[VIEWER] + [
                           'issues.viewopen_issue',
                           'issues.viewopen_proposal',
                           'communities.viewupcoming_community',
                          ]

    permissions[PARTICIPANT] = permissions[OBSERVER] + [
                            'issues.viewextended_proposal',
                          ]
     
    permissions[PROPOSER] = permissions[OBSERVER] + [
                           'issues.add_proposal',
                           'communities.viewupcoming_community',
                           'meetings.view_draft',
                          ]

    permissions[CONTRIBUTOR] = permissions[PROPOSER] + [
                           'issues.add_issue',
                          ]

    permissions[EDITOR] = permissions[CONTRIBUTOR] + [
                           'issues.editopen_issue',
                           'issues.editopen_proposal',
                           'issues.edittask_proposal',
                          ]

    permissions[OPERATOR] = permissions[CONTRIBUTOR] + [
                           'issues.add_issuecomment',
                           'issues.edittask_proposal',
                           'community.editupcoming_community',
                           'community.editparticipants_community',
                           'community.editsummary_community', # ???
                           'community.invite_member',
                          ]

    permissions[DECIDER] = permissions[OPERATOR] + [
                           'issues.editopen_issuecomment',
                           'community.editagenda_community',
                           'issues.acceptopen_proposal',
                           'meetings.add_meeting',  # == Close Meeting
                          ]

    permissions[MANAGER] = permissions[DECIDER] + [
                           'issues.editopen_issue',
                           'issues.editclosed_issue',
                           'issues.editclosed_issuecomment',
                           'issues.editopen_proposal',
                           'issues.editclosed_proposal',
                           'issues.acceptclosed_proposal',
                          ]


class DefaultGroups(object):
    MEMBER = "member"
    BOARD = "board"
    SECRETARY = "secretary"
    CHAIRMAN = "chairman"

    permissions = {}

    permissions[MEMBER] = frozenset(DefaultRoles.permissions[DefaultRoles.OBSERVER])
    permissions[BOARD] = frozenset(DefaultRoles.permissions[DefaultRoles.PROPOSER])
    permissions[SECRETARY] = frozenset(DefaultRoles.permissions[DefaultRoles.OPERATOR])
    permissions[CHAIRMAN] = frozenset(DefaultRoles.permissions[DefaultRoles.DECIDER] +
                                DefaultRoles.permissions[DefaultRoles.EDITOR])
    CHOICES = (
                (MEMBER, _("member")),
                (BOARD, _("board")),
                (SECRETARY, _("secretary")),
                (CHAIRMAN, _("chairman")),
               )

ALL_PERMISSIONS = frozenset(itertools.chain(*DefaultGroups.permissions.values()))