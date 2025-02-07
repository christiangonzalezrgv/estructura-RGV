# app/models_base.py

from django.conf import settings
from django.db import models
from django.db.models.base import ModelBase

print("APP_NAME EN MODELS:", settings.APP_NAME) 

class PrefixedModelBase(ModelBase):
    """
    Metaclase que asigna dinámicamente el nombre de la tabla usando el prefijo definido en settings.APP_NAME.
    Si en el inner Meta del modelo se define 'db_table', no se sobreescribe.
    """

    def __new__(cls, name, bases, attrs, **kwargs):
        # Detectar si en la definición del modelo se estableció un db_table explícito
        meta = attrs.get("Meta", None)
        user_defined_db_table = meta and hasattr(meta, "db_table")

        # Crear la clase del modelo
        new_class = super().__new__(cls, name, bases, attrs, **kwargs)

        # Si el modelo no es abstracto y NO se definió explícitamente un db_table en Meta,
        # se fuerza la asignación del nombre de tabla con el prefijo dinámico.
        if not new_class._meta.abstract and not user_defined_db_table:
            prefix = getattr(settings, "APP_NAME", "default_app").lower()
            new_class._meta.db_table = f"{prefix}_{new_class.__name__.lower()}"

        return new_class


class BaseModel(models.Model, metaclass=PrefixedModelBase):
    """
    Modelo base abstracto que se usará en todos los modelos de la aplicación.
    """

    class Meta:
        abstract = True
