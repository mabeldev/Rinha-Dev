import requests
from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import redirect, render

from apps.utils.auth_utils import check_authentication
from setup.settings import (
    COMMIT_MULTIPLIER,
    GITHUB_GET_REPOSITORIES,
    ISSUES_MULTIPLIER,
    LINES_MULTIPLIER,
    PULLS_MULTIPLIER,
)

from .models import GitRepositorio, Repositorio


def index(request):
    return render(request, "repositorios/index.html")


@check_authentication
def delete_repository(request, repo_id):
    Repositorio.objects.get(id=repo_id).delete()
    messages.info(request, "Repositório deletado com sucesso!")
    return redirect("repositories")


def sync_repository(request):
    url = request.POST.get("repositorio_url")
    form_type = request.POST.get("form_type")

    repo = get_repository_from_api(request, url)
    stats = get_stats_from_api(request, url)

    score = calculate_score(stats)

    if form_type == "add":
        create_repository(request, repo, stats, score)
    else:
        update_repository(request, repo, stats, score)

    return redirect("repositories")


@check_authentication
def list_repositories(request):
    git_repos = list_git_repositories(request)

    git_repos = sorted(git_repos, key=lambda x: x.is_registered, reverse=True)
    db_repos = list_database_repositories(request)

    if not git_repos and not db_repos:
        messages.info(request, "Você ainda não possui nenhum repositório.")

    git_paginator = Paginator(git_repos, 10)
    db_paginator = Paginator(db_repos, 10)

    try:
        git_page = int(request.GET.get("git_page", 1))
        db_page = int(request.GET.get("db_page", 1))
    except ValueError:
        git_page = 1
        db_page = 1

    git_repos = git_paginator.page(git_page)
    db_repos = db_paginator.page(db_page)

    context = {"git_repos": git_repos, "db_repos": db_repos}

    return render(request, "repositorios/repositorios.html", context)


def list_database_repositories(request):
    return request.user.repositorio_set.all()


def list_git_repositories(request):
    response = requests.get(
        GITHUB_GET_REPOSITORIES,
        headers={"Authorization": f"Bearer {request.user.token}"},
    )
    if response.status_code == 200:
        return [process_git_repo(request, repo) for repo in response.json()]
    else:
        return []


def get_repository_from_api(request, url):
    response = requests.get(
        url, headers={"Authorization": f"Bearer {request.user.token}"}
    )

    if response.ok:
        return process_git_repo(request, response.json())

    messages.error("Repositório não encontrado!")
    return redirect("repositories")


def get_stats_from_api(request, url):
    commits = get_commit_count(request, f"{url}/commits")
    lines, languages = get_line_count(request, f"{url}/languages")
    issues = get_issues_count(request, f"{url}/issues?state=closed")
    pulls = get_pulls_count(request, f"{url}/pulls?state=closed")

    return commits, lines, languages, issues, pulls


def process_git_repo(request, data):
    return GitRepositorio(
        repo_id=data["id"],
        name=data["name"],
        owner=data["owner"]["login"],
        description=data["description"],
        url=data["url"],
        stars=data["stargazers_count"],
        is_registered=is_registered(request, data["id"]),
    )


def calculate_score(stats):
    commits, lines, _, issues, pulls = stats

    score = 0
    score += commits * float(COMMIT_MULTIPLIER)
    score += lines * float(LINES_MULTIPLIER)
    score += issues * float(ISSUES_MULTIPLIER)
    score += pulls * float(PULLS_MULTIPLIER)

    return int(score)


def create_repository(request, repo, stats, score):
    commits, lines, languages, issues, pulls = stats

    if not is_registered(request, repo.repo_id):
        Repositorio.objects.create(
            repository_id=repo.repo_id,
            url=repo.url,
            name=repo.name,
            owner=repo.owner,
            added_by=request.user,
            stars=repo.stars,
            languages=languages,
            commit_count=commits,
            line_count=lines,
            issues_count=issues,
            pulls_count=pulls,
            score=score,
        )
        messages.success(request, "Repositório salvo com sucesso!")

    else:
        messages.info(request, "Esse repositório já está cadastrado!")


def update_repository(request, repo, stats, score):
    commits, lines, languages, issues, pulls = stats

    Repositorio.objects.filter(repository_id=repo.repo_id).update(
        stars=repo.stars,
        languages=languages,
        commit_count=commits,
        line_count=lines,
        issues_count=issues,
        pulls_count=pulls,
        score=score,
    )
    messages.success(request, "Repositório atualizado com sucesso!")


def is_registered(request, repo_id):
    return Repositorio.objects.filter(
        repository_id=repo_id, added_by=request.user
    ).exists()


# API requests


def get_commit_count(request, url):
    response = requests.get(
        url, headers={"Authorization": f"Bearer {request.user.token}"}
    )

    if response.ok:
        return sum(
            1
            for c in response.json()
            if c["author"]["login"] == request.user.username
        )


def get_line_count(request, url):
    response = requests.get(
        url, headers={"Authorization": f"Bearer {request.user.token}"}
    )

    if response.ok:
        lines = 0
        languages = []

        for lang, count in response.json().items():
            lines += count
            languages.append(lang)

        return lines, ", ".join(languages)


def get_issues_count(request, url):
    response = requests.get(
        url, headers={"Authorization": f"Bearer {request.user.token}"}
    )

    if response.ok:
        return sum(1 for i in response.json() if i["state"] == "closed")


def get_pulls_count(request, url):
    response = requests.get(
        url, headers={"Authorization": f"Bearer {request.user.token}"}
    )

    if response.ok:
        return len(response.json())
