from django.db import models

class Repositorio(models.Model):
    project_id = models.CharField(max_length=255)
    nome = models.CharField(max_length=255)
    criador = models.CharField(max_length=255)
    linguagens = models.CharField(max_length=255)
    estrelas = models.IntegerField()
    commit_count = models.IntegerField()
    line_count = models.IntegerField()
    closed_issues_count = models.IntegerField()
    pulls_count = models.IntegerField()
    project_url = models.URLField()
    commits_url = models.URLField()
    pulls_url = models.URLField()
    commits_url = models.URLField()
    pulls_url = models.URLField()
    languages_url = models.URLField()
    ativo = models.BooleanField(default=False)
