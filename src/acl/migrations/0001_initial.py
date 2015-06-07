# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('communities', '0009_auto_20150603_1359'),
    ]

    operations = [
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ordinal', models.IntegerField(default=0, verbose_name='ordinal')),
                ('title', models.CharField(unique=True, max_length=200, verbose_name='title')),
                ('based_on', models.CharField(blank=True, max_length=50, null=True, verbose_name='based on', choices=[(b'viewer', 'Viewer'), (b'observer', 'Observer'), (b'participant', 'Participant'), (b'proposer', 'Proposer'), (b'contributor', 'Contributor'), (b'editor', 'Editor'), (b'operator', 'Operator'), (b'decider', 'Decider'), (b'manager', 'Manager')])),
                ('community', models.ForeignKey(verbose_name='Limit to community', blank=True, to='communities.Community', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='RolePermission',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(max_length=100, verbose_name='Permission', choices=[(b'access_community', 'Access Community'), (b'viewupcoming_community', 'View Upcoming Meeting'), (b'viewupcoming_draft', 'View Upcoming Meeting Before Published'), (b'editagenda_community', 'Edit Upcoming Agenda'), (b'editparticipants_community', 'Manage Upcoming Meeting Participants'), (b'editsummary_community', 'Edit Summary'), (b'editupcoming_community', 'Edit Upcoming'), (b'invite_member', 'Invite Member'), (b'acceptclosed_proposal', 'Acceptclosed Proposal'), (b'acceptopen_proposal', 'Acceptopen Proposal'), (b'add_issue', 'Add Issue'), (b'add_issuecomment', 'Add Issuecomment'), (b'add_proposal', 'Add Proposal'), (b'chairman_vote', 'Chairman Vote'), (b'edit_referendum', 'Edit Referendum'), (b'editclosed_issue', 'Edit Closed Issue'), (b'editclosed_issuecomment', 'Edit Closed Issuecomment'), (b'editclosed_proposal', 'Edit Closed Proposal'), (b'editopen_issue', 'Edit Open Issue'), (b'editopen_issuecomment', 'Edit Open Issuecomment'), (b'editopen_proposal', 'Edit Open Proposal'), (b'edittask_proposal', 'Edit Task Proposal'), (b'move_to_referendum', 'Move To Referendum'), (b'proposal_board_vote', 'Proposal Board Vote'), (b'proposal_board_vote_self', 'Proposal Board Vote Self'), (b'view_proposal_in_discussion', 'View Proposal In Discussion'), (b'view_referendum_results', 'View Referendum Results'), (b'view_update_status', 'View Update Status'), (b'view_straw_vote_result', 'View straw vote result'), (b'viewclosed_issue', 'View Closed Issue'), (b'viewclosed_proposal', 'View Closed Proposal'), (b'viewopen_issue', 'View Open Issue'), (b'viewopen_proposal', 'View Open Proposal'), (b'vote', 'Vote'), (b'vote_ranking', 'Vote Ranking'), (b'add_meeting', 'Add Meeting'), (b'view_meeting', 'View Meeting'), (b'show_member_profile', 'Show Member Profile')])),
                ('role', models.ForeignKey(related_name='perms', to='acl.Role')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='rolepermission',
            unique_together=set([('role', 'code')]),
        ),
    ]
