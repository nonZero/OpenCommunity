from collections import defaultdict
from pprint import pprint

ps = [
    'communities.access_community',
    'issues.viewclosed_issue',
    'issues.viewclosed_proposal',
    'meetings.view_meeting',
    'issues.viewopen_issue',
    'issues.viewopen_proposal',
    'communities.viewupcoming_community',
    'issues.vote',
    'issues.proposal_board_vote_self',
    'issues.vote_ranking',
    'issues.view_proposal_in_discussion',
    'communities.viewupcoming_draft',
    'issues.view_referendum_results',
    'issues.view_update_status',
    'issues.view_straw_vote_result',
    'issues.add_proposal',
    'issues.add_issue',
    'issues.editopen_issue',
    'issues.editopen_proposal',
    'issues.edittask_proposal',
    'issues.add_issuecomment',
    'issues.edittask_proposal',
    'community.editupcoming_community',
    'community.editparticipants_community',
    'community.editsummary_community',  # ???
    'community.invite_member',
    'issues.move_to_referendum',
    'issues.proposal_board_vote',
    'issues.editopen_issuecomment',
    'community.editagenda_community',
    'issues.acceptopen_proposal',
    'meetings.add_meeting',  # == Close Meeting
    'issues.edit_referendum',
    'issues.chairman_vote',
    'issues.editopen_issue',
    'issues.editclosed_issue',
    'issues.editclosed_issuecomment',
    'issues.editopen_proposal',
    'issues.editclosed_proposal',
    'issues.acceptclosed_proposal',
    'users.show_member_profile',
]

dd = defaultdict(set)
t = lambda s: s.replace('_', ' ').replace('edit', 'edit ').replace(
    'view', 'view ').title()
for k, v in [p.split('.') for p in ps]:
    dd[k].add((v, t(v), ()))

pprint(dict(dd))