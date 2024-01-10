"""
Django settings for setup project.

Generated by 'django-admin startproject' using Django 5.0.1.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from pathlib import Path, os

from django.contrib.messages import constants as messages
from dotenv import load_dotenv

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# GITHUB SECRETS
GITHUB_CLIENT_ID = str(os.getenv("GITHUB_CLIENT_ID"))
GITHUB_CLIENT_SECRET = str(os.getenv("GITHUB_CLIENT_SECRET"))

# GITHUB PATHS
GITHUB_GET_REPOSITORIES = "https://api.github.com/user/repos"
GITHUB_GET_REPOSITORY = "https://api.github.com/repos/{owner}/{name}"
GITHUB_OAUTH_URL = "https://github.com/login/oauth/"
GITHUB_REDIRECT_URI = "http://localhost:8000/callback"

# GITHUB CONCAT PATHS
GITHUB_GET_USER_CODE = f"{GITHUB_OAUTH_URL}authorize?client_id={GITHUB_CLIENT_ID}&redirect_uri={GITHUB_REDIRECT_URI}&scope=user"
GITHUB_ACCESS_TOKEN_URL = f"{GITHUB_OAUTH_URL}access_token"

COMMIT_MULTIPLIER = os.getenv("COMMIT_MULTIPLIER")
LINES_MULTIPLIER = os.getenv("LINES_MULTIPLIER")
ISSUES_MULTIPLIER = os.getenv("ISSUES_MULTIPLIER")
PULLS_MULTIPLIER = os.getenv("PULLS_MULTIPLIER")

MYSQL_ROOT_PASSWORD = os.getenv("MYSQL_ROOT_PASSWORD")
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE")
MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
MYSQL_HOST = str(os.getenv("MYSQL_HOST"))
MYSQL_PORT = str(os.getenv("MYSQL_PORT"))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = str(os.getenv("SECRET_KEY"))

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["mabeldev.pythonanywhere.com"]


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "apps.usuarios.apps.UsuariosConfig",
    "apps.repositorios.apps.RepositoriosConfig",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "setup.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "setup.wsgi.application"

DOCKER_DB_DIR = "/app/db.sqlite3"

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

# if os.getenv("DOCKER_DB") == "True":
#     DATABASES = {
#         "default": {
#             "ENGINE": "django.db.backends.mysql",
#             "NAME": MYSQL_DATABASE,
#             "USER": MYSQL_USER,
#             "PASSWORD": MYSQL_PASSWORD,  # Senha do MySQL
#             "HOST": MYSQL_HOST,  # Nome do serviço no Docker Compose
#             "PORT": "3306",
#         }
#     }
# else:
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = "pt-br"

TIME_ZONE = "America/Sao_Paulo"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = "/static/"

STATICFILES_DIRS = [os.path.join(BASE_DIR, "setup/static/")]
STATIC_ROOT = os.path.join(BASE_DIR, "static_files/")


# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Custom Auth user
AUTH_USER_MODEL = "usuarios.CustomUser"

# MESSAGES
MESSAGE_TAGS = {
    messages.ERROR: "danger",
    messages.SUCCESS: "success",
    messages.INFO: "warning",
}
