from django.urls import path

from apps.repositorios import views

urlpatterns = [
    path("", views.index, name="index"),
    path("repositorios", views.list_repositories, name="repositorios"),
    path(
        "add_or_update_repositorio",
        views.add_or_update_repository,
        name="add_or_update_repositorio",
    ),
    path(
        "deletar_repositorio/<int:repo_id>",
        views.delete_repository,
        name="deletar_repositorio",
    ),
]
