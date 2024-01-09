from django.urls import path

from apps.usuarios import views

urlpatterns = [
    path("login", views.login, name="login"),
    path("logout", views.logout, name="logout"),
    path("callback/", views.callback, name="github_callback"),
    path("ranking", views.get_users_ranking, name="ranking"),
]
