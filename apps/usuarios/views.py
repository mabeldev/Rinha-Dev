import requests
from django.contrib import auth, messages
from django.core.paginator import EmptyPage, InvalidPage, Paginator
from django.shortcuts import redirect, render

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


def callback(request):
    token = get_access_token(request)
    if not token:
        messages.error(request, "Erro ao obter token do GitHub")
        return redirect("index")

    user_data = get_user_data(token)
    if not user_data:
        messages.error(request, "Erro ao obter dados do usuário")
        return redirect("index")

    user = add_or_update_user(user_data, token)
    authorize_user(request, user)
    return redirect("index")


def get_access_token(request):
    code = request.GET.get("code")
    response = requests.post(
        GITHUB_ACCESS_TOKEN_URL,
        data={
            "client_id": GITHUB_CLIENT_ID,
            "client_secret": GITHUB_CLIENT_SECRET,
            "code": code,
            "redirect_uri": GITHUB_REDIRECT_URI,
        },
        headers={"Accept": "application/json"},
    )
    if response.status_code == 200:
        return response.json()["access_token"]
    return None


def get_user_data(token):
    headers = {"Authorization": f"token {token}"}
    response = requests.get("https://api.github.com/user", headers=headers)
    if response.status_code == 200:
        return response.json()
    return None


def add_or_update_user(user_data, token):
    username = user_data["login"]
    email = user_data["email"]

    user = CustomUser.objects.filter(username=username).first()

    if user:
        user.token = token
        user.save()
    else:
        user = CustomUser.objects.create_user(
            username=username, email=email, token=token
        )
        user.save()
    return user


def authorize_user(request, user):
    try:
        auth.login(request, user)
        messages.success(request, "Login realizado com sucesso")
    except auth.AuthenticationFailed:
        messages.error(request, "Erro ao realizar login")


def get_users_ranking(request):
    users = CustomUser.objects.all()
    score_list = []

    for user in users:
        score = calculate_user_score(user)
        score_list.append(
            {
                "ranking": 0,
                "username": user.username,
                "repo_count": user.repositorio_set.count(),
                "score": score,
            }
        )

    rank_users(score_list)

    paginator = Paginator(score_list, 10)
    try:
        page = int(request.GET.get("page", "1"))
    except ValueError:
        page = 1

    try:
        scores = paginator.page(page)
    except (EmptyPage, InvalidPage):
        scores = paginator.page(paginator.num_pages)

    return render(request, "ranking/ranking.html", {"scores": scores})


def calculate_user_score(user):
    score = 0
    for repo in user.repositorio_set.all():
        score += repo.score
    return score


def rank_users(score_list):
    score_list.sort(key=lambda x: x["score"], reverse=True)
    for i, item in enumerate(score_list):
        item["ranking"] = i + 1
