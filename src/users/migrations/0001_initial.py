# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
import users.models
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
        ('communities', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='OCUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(null=True, verbose_name='last login', blank=True)),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.EmailField(unique=True, max_length=255, verbose_name='email address', db_index=True)),
                ('display_name', models.CharField(max_length=200, verbose_name='Your name')),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('groups', models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Group', blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Permission', blank=True, help_text='Specific permissions for this user.', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
        ),
        migrations.CreateModel(
            name='Invitation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('name', models.CharField(max_length=200, null=True, verbose_name='Name', blank=True)),
                ('email', models.EmailField(max_length=254, verbose_name='Email')),
                ('message', models.TextField(null=True, verbose_name='Message', blank=True)),
                ('code', models.CharField(default=users.models.create_code, max_length=48)),
                ('default_group_name', models.CharField(max_length=50, verbose_name='Group', choices=[(b'member', 'member'), (b'board', 'board'), (b'secretary', 'secretary'), (b'chairman', 'chairman')])),
                ('status', models.PositiveIntegerField(default=0, verbose_name='Status', choices=[(0, 'Pending'), (1, 'Sent'), (2, 'Failed')])),
                ('times_sent', models.PositiveIntegerField(default=0, verbose_name='Times Sent')),
                ('error_count', models.PositiveIntegerField(default=0, verbose_name='Error count')),
                ('last_sent_at', models.DateTimeField(null=True, verbose_name='Sent at', blank=True)),
                ('community', models.ForeignKey(related_name='invitations', verbose_name='Community', to='communities.Community')),
                ('created_by', models.ForeignKey(related_name='invitations_created', verbose_name='Created by', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(related_name='invitations', verbose_name='User', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'verbose_name': 'Invitation',
                'verbose_name_plural': 'Invitations',
            },
        ),
        migrations.CreateModel(
            name='Membership',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('default_group_name', models.CharField(max_length=50, verbose_name='Group', choices=[(b'member', 'member'), (b'board', 'board'), (b'secretary', 'secretary'), (b'chairman', 'chairman')])),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('in_position_since', models.DateField(default=datetime.date(2015, 5, 12), verbose_name='In position since')),
                ('community', models.ForeignKey(related_name='memberships', verbose_name='Community', to='communities.Community')),
                ('invited_by', models.ForeignKey(related_name='members_invited', verbose_name='Invited by', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('user', models.ForeignKey(related_name='memberships', verbose_name='User', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Community Member',
                'verbose_name_plural': 'Community Members',
            },
        ),
        migrations.AlterUniqueTogether(
            name='membership',
            unique_together=set([('community', 'user')]),
        ),
        migrations.AlterUniqueTogether(
            name='invitation',
            unique_together=set([('community', 'email')]),
        ),
    ]
