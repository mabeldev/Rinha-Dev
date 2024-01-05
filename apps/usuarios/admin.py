from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from apps.usuarios.models import CustomUser


class CustomUserAdmin(UserAdmin):
    list_display = (
        "username",
        "email",
        "first_name",
        "last_name",
        "access_token",
    )
    list_editable = ("access_token",)


admin.site.register(CustomUser, CustomUserAdmin)
