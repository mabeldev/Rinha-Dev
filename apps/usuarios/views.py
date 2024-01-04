import webbrowser

import requests
from django.shortcuts import redirect

from setup.settings import (
    GITHUB_ACCESS_TOKEN_URL,
    GITHUB_AUTH_URL,
    GITHUB_CLIENT_ID,
    GITHUB_CLIENT_SECRET,
    GITHUB_REDIRECT_URI,
)


def login(request):
    webbrowser.open(GITHUB_AUTH_URL)
    redirect(url="index")


def callback_view(request):
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
        access_token = response.json()["access_token"]
        print(access_token)
        return redirect(to="index")
    else:
        print("Erro ao obter token de acesso.")
        return redirect(to="index")


def logout(request):
    redirect
    logout(request)
