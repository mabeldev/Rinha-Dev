import requests
from django.contrib import auth, messages
from django.core.paginator import EmptyPage, InvalidPage, Paginator
from django.shortcuts import redirect, render

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


def get_users_ranking(request):
    users = CustomUser.objects.all()
    pontuacoes_list = []

    for user in users:
        pontuacao = 0
        repositorios = Repositorio.objects.filter(added_by=user.username)

        for repositorio in repositorios:
            pontuacao += repositorio.pontuacao

        pontuacoes_list.append(
            {
                "posicao": 0,
                "username": user.username,
                "repo_count": repositorios.count,
                "pontuacao": pontuacao,
            }
        )
    pontuacoes_list = sorted(
        pontuacoes_list, key=lambda x: x["pontuacao"], reverse=True
    )

    for user in pontuacoes_list:
        user["posicao"] = pontuacoes_list.index(user) + 1

    paginator = Paginator(pontuacoes_list, 10)
    try:
        page = int(request.GET.get("page", "1"))
    except ValueError:
        page = 1

    try:
        pontuacoes = paginator.page(page)
    except (EmptyPage, InvalidPage):
        pontuacoes = paginator.page(paginator.num_pages)

    return render(request, "ranking/ranking.html", {"pontuacoes": pontuacoes})
