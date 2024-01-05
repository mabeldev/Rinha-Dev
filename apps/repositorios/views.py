import requests
from django.shortcuts import render

from apps.repositorios.models import Repositorio
from setup.settings import GITHUB_GET_REPOSITORIES


def index(request):
    return render(request, "repositorios/index.html")


def list_repositorio_views(request):
    response = requests.get(
        GITHUB_GET_REPOSITORIES,
        headers={"Authorization": f"Bearer {request.user.access_token}"},
    )
    repositorios = []
    if response.status_code == 200:
        for repo in response.json():
            commits_url = repo["commits_url"].replace("{/sha}", "")
            languages_url = repo["languages_url"]
            issues_url = repo["issues_url"].replace("{/number}", "")
            pulls_url = repo["pulls_url"].replace("{/number}", "")

            get_all_api_requests_datas(
                request, commits_url, languages_url, issues_url, pulls_url
            )

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
            repositorios.append(repositorio)
        return render(
            request,
            "repositorios/repositorios.html",
            {"repositorios": repositorios},
        )
    else:
        print(response.status_code)
        return render(request, "repositorios/repositorios.html")


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
        languages = str(languages)
        languages = (
            languages.replace("'", "").replace("[", "").replace("]", "")
        )
        print(languages)
        return line_count, languages


def get_closed_issues_count(request, issues_url):
    response = requests.get(
        issues_url + "?state=closed",
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
        pulls_url + "?state=closed",
        headers={"Authorization": f"Bearer {request.user.access_token}"},
    )
    if response.status_code == 200:
        pulls_count = 0
        for pull in response.json():
            if pull["state"] == "closed":
                pulls_count += 1
        return pulls_count


def get_all_api_requests_datas(
    request, commits_url, languages_url, issues_url, pulls_url
):
    commits_response = requests.get(
        commits_url,
        headers={"Authorization": f"Bearer {request.user.access_token}"},
    )

    commit_count = 0
    for commit in commits_response.json():
        if commit["commit"]["author"]["email"] == request.user.email:
            commit_count += 1
    return commit_count
