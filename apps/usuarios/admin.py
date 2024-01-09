from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from apps.usuarios.models import CustomUser


class CustomUserAdmin(UserAdmin):
    list_display = (
        "username",
        "email",
    )


admin.site.register(CustomUser, CustomUserAdmin)
