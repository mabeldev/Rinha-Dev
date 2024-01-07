from django.urls import path

from apps.repositorios import views

urlpatterns = [
    path("", views.index, name="index"),
    path("repositorios", views.list_all_repositorios, name="repositorios"),
    path(
        "add_or_update_repositorio",
        views.add_or_update_repositorio,
        name="add_or_update_repositorio",
    ),
    path(
        "deletar_repositorio",
        views.deletar_repositorio,
        name="deletar_repositorio",
    ),
]
