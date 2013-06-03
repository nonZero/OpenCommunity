from communities import models
from django.contrib.admin import site
from django.contrib.admin.options import ModelAdmin
from users.admin import MembershipInline


class CommunityAdmin(ModelAdmin):

    fields = (
              'name',
              )

    inlines = [MembershipInline]


site.register(models.Community, CommunityAdmin)
