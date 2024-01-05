from django.urls import path

from apps.repositorios import views

urlpatterns = [
    path("", views.index, name="index"),
    path("repositorios", views.list_repositorio_views, name="repositorios"),
]
