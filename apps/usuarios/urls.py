from django.urls import path

from apps.usuarios.views import callback_view, login, logout

urlpatterns = [
    path("login", login, name="login"),
    path("logout", logout, name="logout"),
    path("callback/", callback_view, name="github_callback"),
]
