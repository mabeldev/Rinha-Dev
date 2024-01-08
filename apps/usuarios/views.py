import requests
from django.contrib import auth, messages
from django.db.models import Q
from django.shortcuts import redirect

from apps.repositorios.models import Repositorio
from apps.usuarios.models import CustomUser
from setup.settings import (
    GITHUB_ACCESS_TOKEN_URL,
    GITHUB_CLIENT_ID,
    GITHUB_CLIENT_SECRET,
    GITHUB_GET_USER_CODE,
    GITHUB_REDIRECT_URI,
)


def login(request):
    return redirect(GITHUB_GET_USER_CODE)


def logout(request):
    auth.logout(request)
    messages.success(request, "Logout efetuado com sucesso!")
    return redirect("index")


def callback_view(request):
    access_token = get_user_token(request)

    if not access_token:
        messages.error(request, "Erro ao tentar realizar login com o Github")
        return redirect("index")

    user_data = get_user_data_json(access_token)

    if not user_data:
        messages.error(request, "Erro ao tentar realizar login com o Github")
        return redirect("index")

    usuario = add_or_update_user(user_data, access_token)
    authorize_user(request, usuario)
    return redirect("index")


def get_user_data_json(access_token):
    headers = {
        "Authorization": f"token {access_token}",
        "Accept": "application/json",
    }
    user_data = requests.get("https://api.github.com/user", headers=headers)

    if user_data.status_code == 200:
        return user_data.json()
    else:
        return None


def get_user_token(request):
    code = request.GET.get("code")

    payload = {
        "client_id": GITHUB_CLIENT_ID,
        "client_secret": GITHUB_CLIENT_SECRET,
        "code": code,
        "redirect_uri": GITHUB_REDIRECT_URI,
    }

    response = requests.post(
        GITHUB_ACCESS_TOKEN_URL,
        data=payload,
        headers={"Accept": "application/json"},
    )

    if response.status_code == 200:
        access_token = str(response.json()["access_token"])
        return access_token
    else:
        return None


def add_or_update_user(user_data, access_token):
    username = user_data["login"]
    email = user_data["email"]

    usuario = CustomUser.objects.filter(email=email).first()
    if usuario:
        usuario.access_token = access_token
        usuario.save()
    else:
        usuario = CustomUser.objects.create_user(
            username=username,
            email=email,
            access_token=access_token,
        )
        usuario.save()
    return usuario


def authorize_user(request, usuario):
    try:
        auth.login(request, usuario)
        messages.success(request, "Login realizado com sucesso")
    except auth.AuthenticationFailed:
        messages.error(request, "Erro ao tentar realizar login")


# def get_users_ranking(request):
#     users = CustomUser.objects.all()
#     for user in users:
#         repositorios = Repositorio.objects.filter(
#             Q(owner=user.username) | Q(added_by=user.username)
#         )

#         pontuacao = 0
#         for repositorio in repositorios:


#     return render(request, "usuarios/ranking.html", {"users": users})
