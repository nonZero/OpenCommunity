from django.contrib import admin
from django.contrib.admin import site
from meetings import models


class AgendaItemInline(admin.TabularInline):
    model = models.AgendaItem
    extra = 0


class MeetingParticipantInline(admin.TabularInline):
    model = models.MeetingParticipant
    extra = 0


class MeetingExternalParticipantInline(admin.TabularInline):
    model = models.MeetingExternalParticipant
    extra = 0


class MeetingAdmin(admin.ModelAdmin):
    inlines = [
        MeetingParticipantInline,
        MeetingExternalParticipantInline,
        AgendaItemInline,
    ]

    list_display = (
                    '__unicode__',
                    'community',
                    )
    
    list_filter = (
                        'community',
                        'participants',
                        'guests',
                        )

site.register(models.Meeting, MeetingAdmin)
site.register(models.AgendaItem)
