# app/apps.py

from django.apps import AppConfig
from django.conf import settings
from django.apps import apps



class CoreConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "app"
    label = settings.APP_NAME
