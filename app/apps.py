# app/apps.py

from django.apps import AppConfig
from django.conf import settings
from django.apps import apps



class CoreConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "app"
    label = settings.APP_NAME

    def ready(self):
        # Este método se ejecuta cuando Django ha cargado todos los modelos
        global TABLE_NAMES
        TABLE_NAMES = self.get_table_names()

    @staticmethod
    def get_table_names():
        """Obtiene los nombres de las tablas de la base de datos."""
        models = apps.get_models()
        return [model._meta.db_table for model in models]
