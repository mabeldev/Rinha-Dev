import requests
from django.contrib import messages
from django.shortcuts import redirect, render

from apps.repositorios.models import GitRepositorio, Repositorio
from setup.settings import GITHUB_GET_REPOSITORIES


def index(request):
    return render(request, "repositorios/index.html")


def cadastrar_repositorio(request):
    if request.method == "POST":
        repositorio_id = request.POST.get("repositorio_id")
        repositorio_nome = request.POST.get("repositorio_nome")
        repositorio_criador = request.POST.get("repositorio_criador")
        repositorio_stars = request.POST.get("repositorio_stars")
        repositorio_url = request.POST.get("repositorio_url")
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

        Repositorio.objects.create(
            repository_id=repositorio_id,
            name=repositorio_nome,
            owner=repositorio_criador,
            languages=languages,
            stars=repositorio_stars,
            commit_count=commits_count,
            line_count=line_count,
            issues_count=issues_count,
            pulls_count=pulls_count,
        )
        messages.success(request, "Repositório cadastrado com sucesso!")
    return redirect("repositorios")


def list_repositorio(request):
    repositorios = Repositorio.objects.filter(owner=request.user)
    return render(
        request,
        "repositorios/repositorios.html",
        {"repositorios": repositorios},
    )


def list_git_repositorio(request):
    response = requests.get(
        GITHUB_GET_REPOSITORIES,
        headers={"Authorization": f"Bearer {request.user.access_token}"},
    )
    if response.status_code == 200:
        repositorios_json = response.json()
        repositorios = []

        for repo in repositorios_json:
            repositorio = process_git_repository(repo)
            repositorios.append(repositorio)

        return render(
            request,
            "repositorios/git_repositorios.html",
            {"repositorios": repositorios},
        )
    else:
        messages.error = f"Erro ao buscar repositórios: {response.status_code}"
        return redirect("index")


def process_git_repository(repo):
    git_repositorio = GitRepositorio(
        repository_id=repo["id"],
        name=repo["name"],
        owner=repo["owner"]["login"],
        description=repo["description"],
        url=repo["url"],
        stars=repo["stargazers_count"],
    )
    if Repositorio.objects.filter(
        repository_id=git_repositorio.repository_id
    ).exists():
        git_repositorio.is_registred = True
    else:
        git_repositorio.is_registred = False

    return git_repositorio


def process_repository(request, repo):
    commits_url = repo["commits_url"].replace("{/sha}", "")
    languages_url = repo["languages_url"]
    issues_url = repo["issues_url"].replace("{/number}", "")
    pulls_url = repo["pulls_url"].replace("{/number}", "")

    commit_count = get_commit_count(request, commits_url)
    line_count, languages = get_line_count(request, languages_url)
    closed_issues = get_closed_issues_count(request, issues_url)
    pulls_count = get_pulls_count(request, pulls_url)

    repositorio = Repositorio(
        nome=repo["name"],
        project_id=repo["id"],
        criador=repo["owner"]["login"],
        project_url=repo["html_url"],
        linguagens=languages,
        commits_url=commits_url,
        pulls_url=pulls_url,
        languages_url=languages_url,
        commit_count=commit_count,
        line_count=line_count,
        closed_issues_count=closed_issues,
        pulls_count=pulls_count,
        estrelas=repo["stargazers_count"],
    )
    return repositorio


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
