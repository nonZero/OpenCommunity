from django.contrib import admin
from django.contrib.admin import site
from meetings import models


class AgendaItemInline(admin.TabularInline):
    model = models.AgendaItem
    extra = 0


class MeetingExternalParticipantInline(admin.TabularInline):
    model = models.MeetingExternalParticipant
    extra = 0


class MeetingAdmin(admin.ModelAdmin):
    inlines = [
        MeetingExternalParticipantInline,
        AgendaItemInline,
    ]

site.register(models.Meeting, MeetingAdmin)
site.register(models.AgendaItem)
