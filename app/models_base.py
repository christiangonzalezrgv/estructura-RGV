# app/models_base.py


from django.conf import settings
from django.db import models
from django.db.models.base import ModelBase

class PrefixedModelBase(ModelBase):
    """
    Metaclase que asigna dinámicamente el nombre de la tabla usando el prefijo definido en settings.APP_NAME.
    """

    def __new__(cls, name, bases, attrs, **kwargs):
        # Crear la nueva clase del modelo
        new_class = super().__new__(cls, name, bases, attrs, **kwargs)

        # Si el modelo no es abstracto, establecer db_table
        if not new_class._meta.abstract:
            prefix = getattr(settings, "APP_NAME", "default_app").lower()
            new_table_name = f"{prefix}_{new_class.__name__.lower()}"
            new_class._meta.db_table = new_table_name

        return new_class


class BaseModel(models.Model, metaclass=PrefixedModelBase):
    """
    Modelo base abstracto que se usará en todos los modelos de la aplicación.
    """

    class Meta:
        abstract = True
