from django.urls import path

from apps.repositorios import views

urlpatterns = [
    path("", views.index, name="index"),
    path("repositories", views.list_repositories, name="repositories"),
    path(
        "sync_repository",
        views.sync_repository,
        name="sync_repository",
    ),
    path(
        "delete_repository/<int:repo_id>",
        views.delete_repository,
        name="delete_repository",
    ),
]
