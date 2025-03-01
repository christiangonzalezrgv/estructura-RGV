# config/settings.py

import os
from pathlib import Path

from dotenv import load_dotenv
from django.apps import apps

# Definir el prefijo de la aplicación a partir de APP_NAME (en minúsculas)
APP_PREFIX = os.getenv("APP_NAME", "default_app").lower()

# -----------------------------
# MONKEY PATCH: Sobrescribir la propiedad db_table en Options
# para que todos los modelos (incluidos los de Django) usen el prefijo APP_PREFIX.
from django.db.models.options import Options


def new_db_table(self):
    """
    Devuelve el nombre de la tabla con el prefijo APP_PREFIX.
    Si self._db_table ya fue asignado, se usa ese valor; en caso contrario,
    se genera el nombre por defecto (app_label + "_" + model_name) y se le antepone el prefijo.
    """
    table = self._db_table if self._db_table else f"{self.app_label}_{self.model_name}"
    if not table.startswith(f"{APP_PREFIX}_"):
        table = f"{APP_PREFIX}_{table}"
    return table


def set_db_table(self, value):
    self._db_table = value


Options.db_table = property(new_db_table, set_db_table)
# -----------------------------

# Directorio base del proyecto
BASE_DIR = Path(__file__).resolve().parent.parent

# Cargar variables de entorno desde .env
load_dotenv(os.path.join(BASE_DIR, ".env"))

# Configuración de la aplicación
SECRET_KEY = os.getenv("SECRET_KEY", "django-insecure-default-key")
DEBUG = os.getenv("DEBUG", "True") == "True"

# Variable para el prefijo de la aplicación (se usará también para el label de la app)
APP_NAME = os.getenv("APP_NAME", "default_app").lower()

# Hosts permitidos
ALLOWED_HOSTS = os.getenv(
    "ALLOWED_HOSTS",
    "127.0.0.1,localhost,django-prueba.eba-uryewyx3.us-east-2.elasticbeanstalk.com,172.31.40.205",
).split(",")

# Aplicaciones instaladas
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "app",
    "auditlog",
    "widget_tweaks"
]

# Middleware
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "auditlog.middleware.AuditlogMiddleware",
]

# Configuración para Django Auditlog: incluye todos los modelos para la auditoría.
AUDITLOG_INCLUDE_ALL_MODELS = True

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
                "app.context_processors.table_names",
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
        "NAME": "estructura_django_db",
        "USER": "postgres",
        "PASSWORD": "MyGPUeZVeeaTrWUE8xrZ",
        "HOST": "estructura-django-db.cbgwwkuui0z9.us-east-2.rds.amazonaws.com",
        "PORT": 5432,
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
# Usamos una ruta absoluta para STATIC_ROOT para que collectstatic los recopile correctamente
STATIC_ROOT = BASE_DIR / "staticfiles"
# Configuración de almacenamiento de archivos estáticos con compresión y cacheo
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# Configuración de archivos de medios (subidos por usuarios)
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# Configuración del campo por defecto en modelos
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Rutas de redirección después del login/logout
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/authentication/login/"

# Configurar el modelo de usuario personalizado
AUTH_USER_MODEL = f"{APP_NAME}.Usuario"

#Variables para subir archivos a S3
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID", "AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY", "AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_REGION", "AWS_REGION")
AWS_S3_BUCKET_NAME = os.getenv("AWS_S3_BUCKET_NAME", "AWS_S3_BUCKET_NAME")
profile = os.getenv("profile", "profile")

APPEND_SLASH=False
