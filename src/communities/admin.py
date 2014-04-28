from communities import models
from django.contrib.admin import site
from django.contrib.admin.options import ModelAdmin, TabularInline
from users.models import Membership


class CommunityGroupInline(TabularInline):
    model = models.CommunityGroup


class CommunityMembershipInline(TabularInline):
    model = Membership
    fk_name = 'community'


class CommunityAdmin(ModelAdmin):

    fields = (
              'name',
              'board_name',
              'official_identifier',
              'logo',
              'is_public',
              'straw_voting_enabled',
              'issue_ranking_enabled',
              'allow_links_in_emails',
              'register_missing_board_members',
              'email_invitees',
              )

    inlines = [
        CommunityGroupInline,
        CommunityMembershipInline,
    ]

# class CommunityGroupRoleInline(TabularInline):
#     model = models.CommunityGroupRole

class CommunityGroupAdmin(ModelAdmin):
    pass
    # inlines = [
    #     CommunityGroupRoleInline,
    # ]




site.register(models.Community, CommunityAdmin)
site.register(models.CommunityGroup, CommunityGroupAdmin)
# site.register(models.CommunityGroupRole)
