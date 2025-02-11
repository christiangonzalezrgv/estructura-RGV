from django.apps import apps

def table_names(request):
    """Devuelve los nombres de las tablas para todas las plantillas."""
    models = apps.get_models()
    table_names = [model._meta.db_table for model in models]
    return {'TABLE_NAMES': table_names}