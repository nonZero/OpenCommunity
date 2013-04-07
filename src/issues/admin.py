from django.contrib import admin
from django.contrib.admin import site
from issues import models


class ProposalInline(admin.TabularInline):
    model = models.Proposal
    extra = 0


class IssueAdmin(admin.ModelAdmin):
    inlines = [
        ProposalInline,
    ]
site.register(models.Issue, IssueAdmin)
site.register(models.Proposal)
site.register(models.ProposalVote)
