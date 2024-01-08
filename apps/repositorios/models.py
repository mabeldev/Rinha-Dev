from django.db import models


class Repositorio(models.Model):
    repository_id = models.IntegerField()
    url = models.URLField(max_length=255)
    name = models.CharField(max_length=255)
    owner = models.CharField(max_length=255)
    added_by = models.CharField(max_length=255)
    stars = models.IntegerField()
    languages = models.CharField(max_length=255)
    commit_count = models.IntegerField()
    line_count = models.IntegerField()
    issues_count = models.IntegerField()
    pulls_count = models.IntegerField()


class GitRepositorio:
    def __init__(self, repository_id, name, owner, description, stars, url):
        self.repository_id = repository_id
        self.name = name
        self.owner = owner
        self.description = description
        self.stars = stars
        self.url = url
        is_registred = False
