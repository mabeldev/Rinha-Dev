from django.db import models


class Repositorio(models.Model):
    repository_id = models.IntegerField()
    url = models.URLField(max_length=255)
    name = models.CharField(max_length=255)
    owner = models.CharField(max_length=255)
    added_by = models.ForeignKey(
        "usuarios.CustomUser", on_delete=models.CASCADE
    )
    stars = models.IntegerField()
    languages = models.CharField(max_length=255)
    commit_count = models.IntegerField()
    line_count = models.IntegerField()
    issues_count = models.IntegerField()
    pulls_count = models.IntegerField()
    score = models.IntegerField()


class GitRepositorio:
    def __init__(
        self,
        repo_id: int,
        name: str,
        owner: str,
        description: str,
        stars: int,
        url: str,
        is_registered: bool = False,
    ):
        self.repo_id = repo_id
        self.name = name
        self.owner = owner
        self.description = description
        self.stars = stars
        self.url = url
        self.is_registered = is_registered
