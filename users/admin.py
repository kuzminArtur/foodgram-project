from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from django.contrib.auth import get_user_model

User = get_user_model()

admin.site.unregister(User)


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_filter = (
        'is_staff', 'is_superuser', 'is_active', 'groups', 'email', 'username'
    )
