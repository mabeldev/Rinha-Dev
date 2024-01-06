from django.urls import path

from apps.repositorios import views

urlpatterns = [
    path("", views.index, name="index"),
    path(
        "git_repositorios",
        views.list_git_repositorio,
        name="git_repositorios",
    ),
    path("repositorios", views.list_repositorio, name="repositorios"),
    path("cadastrar_repositorio", views.cadastrar_repositorio, name="cadastrar_repositorio"),
]
