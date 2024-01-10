from django.contrib.auth.models import AbstractUser
from django.db import models

from apps.repositorios.models import Repositorio


class CustomUser(AbstractUser):
    token = models.CharField(max_length=255)
    repositorios = models.ManyToManyField(Repositorio)
