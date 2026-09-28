from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    ordering = ('email',)
    list_display = (
        'email',
        'first_name',
        'last_name',
        'is_active',
        'is_staff',
        'is_admin',
        'is_verified',
    )
    search_fields = ('email', 'first_name', 'last_name')

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (
            'Personal info',
            {
                'fields': (
                    'first_name',
                    'last_name',
                    'phone_number',
                    'is_verified',
                )
            },
        ),
        (
            'Permissions',
            {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_admin',
                    'is_superuser',
                    'groups',
                    'user_permissions',
                )
            },
        ),
        (
            'JWT',
            {
                'fields': (
                    'token_last_expired',
                    'token_revoked_at',
                )
            },
        ),
    )

    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': (
                    'email',
                    'password1',
                    'password2',
                    'first_name',
                    'last_name',
                    'phone_number',
                    'is_active',
                    'is_staff',
                    'is_admin',
                    'is_superuser',
                ),
            },
        ),
    )
