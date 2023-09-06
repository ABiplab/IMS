from django.contrib import admin
from .models import *
# Register your models here.
@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ['id', 'name',]

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'display_roles')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'roles__name')
    list_filter = ('roles__name', )

    def display_roles(self, obj):
        return ", ".join([role.name for role in obj.roles.all()])

    display_roles.short_description = 'Roles'