# app/models.py

from django.db import models

from .models_base import BaseModel


class Usuario(BaseModel):
    """
    Modelo de Usuario. La tabla se generará automáticamente como:
    "estructura_rgv_usuario" (suponiendo que APP_NAME=estructura_rgv)
    """

    nombre = models.CharField(max_length=100)
    correo = models.EmailField(unique=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"


class LogAuditoria(BaseModel):
    """
    Modelo para registrar logs de auditoría.
    La tabla se nombrará "<APP_NAME>_logauditoria".
    """

    accion = models.CharField(max_length=200)
    fecha = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.fecha} - {self.accion}"

    class Meta:
        verbose_name = "Log de Auditoría"
        verbose_name_plural = "Logs de Auditoría"
