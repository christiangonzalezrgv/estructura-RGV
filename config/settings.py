# config/settings.py

import os
from pathlib import Path
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

# Directorio base del proyecto
BASE_DIR = Path(__file__).resolve().parent.parent

# Configuración de la aplicación
SECRET_KEY = os.getenv("SECRET_KEY", "django-insecure-default-key")
DEBUG = os.getenv("DEBUG", "True") == "True"

# Variable para el prefijo de la aplicación
APP_NAME = os.getenv("APP_NAME", "default_app").lower()

# Hosts permitidos
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "127.0.0.1,localhost").split(",")

# Aplicaciones instaladas
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "app",
]

# Middleware
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# Configuración de URLs raíz
ROOT_URLCONF = "config.urls"

# Configuración de Templates
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "app/templates"],
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

# Configuración del WSGI
WSGI_APPLICATION = "config.wsgi.application"

# Configuración de Base de Datos con PostgreSQL
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("DATABASE_NAME", "mydatabase"),
        "USER": os.getenv("DATABASE_USER", "myuser"),
        "PASSWORD": os.getenv("DATABASE_PASSWORD", "mypassword"),
        "HOST": os.getenv("DATABASE_HOST", "localhost"),
        "PORT": os.getenv("DATABASE_PORT", "5432"),
    }
}

# Validadores de contraseñas
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# Internacionalización
LANGUAGE_CODE = "es-mx"

TIME_ZONE = "America/Mexico_City"

USE_I18N = True
USE_TZ = True

# Configuración de archivos estáticos (CSS, JS, imágenes)
STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "app/static"]
STATIC_ROOT = BASE_DIR / "staticfiles"

# Configuración de archivos de medios (subidos por usuarios)
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# Configuración del campo por defecto en modelos
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

'''
Agregar esto para que solo se realicen las migraciones de la app actual

MIGRATION_MODULES = {
    "auth": None,
    "contenttypes": None,
    "sessions": None,
    "admin": None,
}
'''