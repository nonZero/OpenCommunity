# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('meetings', '0001_initial'),
        ('issues', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='voteresult',
            name='meeting',
            field=models.ForeignKey(to='meetings.Meeting'),
        ),
        migrations.AddField(
            model_name='voteresult',
            name='proposal',
            field=models.ForeignKey(related_name='results', to='issues.Proposal'),
        ),
        migrations.AddField(
            model_name='proposalvoteboard',
            name='proposal',
            field=models.ForeignKey(to='issues.Proposal'),
        ),
    ]
