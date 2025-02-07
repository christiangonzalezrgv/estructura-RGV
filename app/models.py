# app/models.py

from django.db import models
from django.conf import settings
from .models_base import BaseModel


class Usuario(BaseModel):
    """
    Modelo de Usuario. La tabla se generará automáticamente como:
    """

    nombre = models.CharField(max_length=100)
    correo = models.EmailField(unique=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"
        app_label = settings.APP_NAME


class LogAuditoria(BaseModel):
    """
    Modelo para registrar logs de auditoría.
    """

    accion = models.CharField(max_length=200)
    fecha = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.fecha} - {self.accion}"

    class Meta:
        verbose_name = "Log de Auditoría"
        verbose_name_plural = "Logs de Auditoría"
        app_label = settings.APP_NAME
