from django.contrib import admin
from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'first_name', 'last_name', 'is_active', 'is_admin', 'is_staff', 'is_superuser')
    search_fields = ('email', 'first_name', 'last_name')
    list_filter = ('is_active', 'is_admin', 'is_staff', 'is_superuser', 'is_verified')
