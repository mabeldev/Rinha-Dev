from django.contrib import admin

# Register your models here.
from .models import Repositorio


class RepositorioAdmin(admin.ModelAdmin):
    list_display = ("name", "owner", "added_by")
    search_fields = (
        "owner",
        "added_by",
    )


admin.site.register(Repositorio, RepositorioAdmin)
