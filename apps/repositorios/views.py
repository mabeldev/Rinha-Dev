import requests
from django.contrib import messages
from django.core.paginator import EmptyPage, InvalidPage, Paginator
from django.db.models import Q
from django.shortcuts import redirect, render

from apps.repositorios.models import GitRepositorio, Repositorio
from apps.utils.auth_utils import check_authentication
from setup.settings import (
    COMMIT_MULTIPLIER,
    GITHUB_GET_REPOSITORIES,
    ISSUES_MULTIPLIER,
    LINES_MULTIPLIER,
    PULLS_MULTIPLIER,
)


def index(request):
    return render(request, "repositorios/index.html")


@check_authentication
def deletar_repositorio(request):
    repositorio_id = request.POST.get("repositorio_id")
    repositorio = Repositorio.objects.get(id=repositorio_id)
    repositorio.delete()
    messages.info(request, "Repositório deletado com sucesso!")
    return redirect("repositorios")


def add_or_update_repositorio(request):
    repositorio_url = request.POST.get("repositorio_url")
    form_type = request.POST.get("form_type")

    repositorio = get_repositorio_by_api(request, repositorio_url)
    (
        commits_count,
        line_count,
        languages,
        issues_count,
        pulls_count,
    ) = get_dates_by_api_request(request, repositorio_url)

    pontuacao = 0
    pontuacao += commits_count * float(COMMIT_MULTIPLIER)
    pontuacao += line_count * float(LINES_MULTIPLIER)
    pontuacao += issues_count * float(ISSUES_MULTIPLIER)
    pontuacao += pulls_count * float(PULLS_MULTIPLIER)

    if form_type == "add":
        Repositorio.objects.create(
            repository_id=repositorio.repository_id,
            url=repositorio.url,
            name=repositorio.name,
            owner=repositorio.owner,
            added_by=request.user,
            stars=repositorio.stars,
            languages=languages,
            commit_count=commits_count,
            line_count=line_count,
            issues_count=issues_count,
            pulls_count=pulls_count,
            pontuacao=pontuacao,
        )
        messages.success(request, "Repositório cadastrado com sucesso!")
    else:
        Repositorio.objects.filter(
            repository_id=repositorio.repository_id
        ).update(
            stars=repositorio.stars,
            languages=languages,
            commit_count=commits_count,
            line_count=line_count,
            issues_count=issues_count,
            pulls_count=pulls_count,
            pontuacao=pontuacao,
        )
        messages.success(request, "Repositório atualizado com sucesso!")
    return redirect("repositorios")


def get_dates_by_api_request(request, repositorio_url):
    commits_count = get_commit_count(request, f"{repositorio_url}/commits")
    line_count, languages = get_line_count(
        request, f"{repositorio_url}/languages"
    )
    issues_count = get_issues_count(
        request, f"{repositorio_url}/issues?state=closed"
    )
    pulls_count = get_pulls_count(
        request, f"{repositorio_url}/pulls?state=closed"
    )

    return commits_count, line_count, languages, issues_count, pulls_count


def get_repositorio_by_api(request, repositorio_url):
    response = requests.get(
        f"{repositorio_url}",
        headers={"Authorization": f"Bearer {request.user.access_token}"},
    )
    if response.status_code == 200:
        repositorio_json = response.json()
        repositorio = process_git_repository(request, repositorio_json)
        return repositorio
    else:
        messages.error(request, "Repositório não encontrado!")
        return redirect("repositorios")


@check_authentication
def list_all_repositorios(request):
    repositorios_git = list(list_git_repositorio(request))
    repositorios_git.sort(key=lambda x: x.is_registred, reverse=True)

    repositoios_db = list(list_repositorio(request))

    if not repositorios_git and not repositoios_db:
        messages.info(request, "Você ainda não possui nenhum repositório.")

    paginator_git = Paginator(repositorios_git, 8)
    paginator_db = Paginator(repositoios_db, 8)

    try:
        page_git = request.GET.get("page_git")
    except ValueError:
        page_git = 1

    try:
        page_db = request.GET.get("page_db")
    except ValueError:
        page_db = 1

    try:
        repositorios_paginated_git = paginator_git.get_page(page_git)
    except (EmptyPage, InvalidPage):
        repositorios_paginated_git = paginator_git.page(1)

    try:
        repositorios_paginated_db = paginator_db.get_page(page_db)
    except (EmptyPage, InvalidPage):
        repositorios_paginated_db = paginator_db.page(1)

    return render(
        request,
        "repositorios/repositorios.html",
        {
            "repositorios_git": repositorios_paginated_git,
            "repositorios_db": repositorios_paginated_db,
        },
    )


def list_repositorio(request):
    repositorios = Repositorio.objects.filter(
        Q(owner=request.user) | Q(added_by=request.user)
    )

    return repositorios


def list_git_repositorio(request):
    response = requests.get(
        GITHUB_GET_REPOSITORIES,
        headers={"Authorization": f"Bearer {request.user.access_token}"},
    )
    if response.status_code == 200:
        repositorios_json = response.json()
        repositorios = []

        for repo in repositorios_json:
            repositorio = process_git_repository(request, repo)
            repositorios.append(repositorio)
        if not repositorios:
            return None
        return repositorios
    else:
        messages.error = f"Erro ao buscar repositórios: {response.status_code}"
        return None


def process_git_repository(request, repo):
    git_repositorio = GitRepositorio(
        repository_id=repo["id"],
        name=repo["name"],
        owner=repo["owner"]["login"],
        description=repo["description"],
        url=repo["url"],
        stars=repo["stargazers_count"],
    )
    if Repositorio.objects.filter(
        Q(repository_id=git_repositorio.repository_id)
        & Q(added_by=request.user)
    ).exists():
        git_repositorio.is_registred = True
    else:
        git_repositorio.is_registred = False

    return git_repositorio


def get_commit_count(request, commits_url):
    response = requests.get(
        commits_url,
        headers={"Authorization": f"Bearer {request.user.access_token}"},
    )
    if response.status_code == 200:
        commit_count = 0
        for commit in response.json():
            if commit["commit"]["author"]["email"] == request.user.email:
                commit_count += 1
        return commit_count


def get_line_count(request, languages_url):
    response = requests.get(
        languages_url,
        headers={"Authorization": f"Bearer {request.user.access_token}"},
    )
    if response.status_code == 200:
        line_count = 0
        languages = []
        for language, lines in response.json().items():
            line_count += lines
            languages.append(language)
        languages = (
            str(languages).replace("'", "").replace("[", "").replace("]", "")
        )
        return line_count, languages


def get_issues_count(request, issues_url):
    response = requests.get(
        issues_url,
        headers={"Authorization": f"Bearer {request.user.access_token}"},
    )
    if response.status_code == 200:
        closed_issues_count = 0
        for issue in response.json():
            if issue["state"] == "closed":
                closed_issues_count += 1
        return closed_issues_count


def get_pulls_count(request, pulls_url):
    response = requests.get(
        pulls_url,
        headers={"Authorization": f"Bearer {request.user.access_token}"},
    )
    if response.status_code == 200:
        pulls_count = 0
        for pull in response.json():
            pulls_count += 1
        return pulls_count
