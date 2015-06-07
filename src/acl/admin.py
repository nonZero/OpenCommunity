from acl import models
from django.contrib import admin


class RolePermissionInline(admin.TabularInline):
    model = models.RolePermission


class RoleAdmin(admin.ModelAdmin):
    list_display = ['community', 'title', 'based_on']
    inlines = [
        RolePermissionInline
    ]


admin.site.register(models.Role, RoleAdmin)
