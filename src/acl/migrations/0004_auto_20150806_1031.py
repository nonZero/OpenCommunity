# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('acl', '0003_auto_20150615_1421'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rolepermission',
            name='code',
            field=models.CharField(max_length=100, verbose_name='Permission', choices=[(b'access_community', 'Access Community'), (b'viewupcoming_community', 'View Upcoming Meeting'), (b'viewupcoming_draft', 'View Upcoming Meeting Before Published'), (b'editagenda_community', 'Edit Upcoming Agenda'), (b'editparticipants_community', 'Manage Upcoming Meeting Participants'), (b'editsummary_community', 'Edit Summary'), (b'editupcoming_community', 'Edit Upcoming'), (b'invite_member', 'Invite Member'), (b'acceptclosed_proposal', 'Acceptclosed Proposal'), (b'acceptopen_proposal', 'Acceptopen Proposal'), (b'add_issue', 'Add Issue'), (b'add_issuecomment', 'Add Issuecomment'), (b'add_proposal', 'Add Proposal'), (b'chairman_vote', 'Chairman Vote'), (b'edit_referendum', 'Edit Referendum'), (b'editclosed_issue', 'Edit Closed Issue'), (b'editclosed_issuecomment', 'Edit Closed Issuecomment'), (b'editclosed_proposal', 'Edit Closed Proposal'), (b'editopen_issue', 'Edit Open Issue'), (b'editopen_issuecomment', 'Edit Open Issuecomment'), (b'editopen_proposal', 'Edit Open Proposal'), (b'edittask_proposal', 'Edit Task Proposal'), (b'move_to_referendum', 'Move To Referendum'), (b'proposal_board_vote', 'Proposal Board Vote'), (b'proposal_board_vote_self', 'Proposal Board Vote Self'), (b'view_proposal_in_discussion', 'View Proposal In Discussion'), (b'view_referendum_results', 'View Referendum Results'), (b'view_update_status', 'View Update Status'), (b'view_straw_vote_result', 'View straw vote result'), (b'viewclosed_issue', 'View Closed Issue'), (b'viewclosed_proposal', 'View Closed Proposal'), (b'viewopen_issue', 'View Open Issue'), (b'viewopen_proposal', 'View Open Proposal'), (b'vote', 'Vote'), (b'vote_ranking', 'Vote Ranking'), (b'add_meeting', 'Add Meeting'), (b'view_meeting', 'View Meeting'), (b'show_member_profile', 'Show Member Profile'), (b'view_confidential', 'Can view confidential Issue/Proposal')]),
        ),
    ]
