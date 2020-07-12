from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from core import models


class UserAdmin(BaseUserAdmin):
    ordering = ['id']
    list_display = ['email', 'name', 'is_active', 'custom_group']
    list_filter = ['groups', 'is_staff', 'is_superuser', 'is_active']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal Info'), {'fields': ('name',)}),
        (
            _('Permissions'),
            {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser',
                )
            }
        ),
        (_('Important dates'), {'fields': ('last_login',)}),
        )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')
            }),
        )

    def custom_group(self, obj):
        # get group, separate by comma, and display empty string if user has no group
        return ','.join([g.name for g in obj.groups.all()]) if obj.groups.count() else ''


admin.site.register(models.User, UserAdmin)
