# app/models.py

from django.conf import settings
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models
from django.utils.timezone import now
import uuid

from .models_base import BaseModel


class UsuarioManager(BaseUserManager):
    """
    Gestor de usuarios personalizado para usar el correo como identificador único.
    """

    def create_user(self, correo, nombre, password=None, **extra_fields):
        """
        Crea y guarda un usuario con el correo, nombre y contraseña proporcionados.
        """
        if not correo:
            raise ValueError("El usuario debe tener un correo electrónico")
        correo = self.normalize_email(correo)
        user = self.model(correo=correo, nombre=nombre, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, correo, nombre, password=None, **extra_fields):
        """
        Crea y guarda un superusuario con el correo, nombre y contraseña proporcionados.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        if extra_fields.get("is_staff") is not True:
            raise ValueError("El superusuario debe tener is_staff=True")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("El superusuario debe tener is_superuser=True")
        return self.create_user(correo, nombre, password, **extra_fields)


class Usuario(AbstractBaseUser, PermissionsMixin, BaseModel):
    """
    Modelo de Usuario personalizado que usa el correo electrónico como identificador.
    Se define explícitamente el campo 'password' para asegurar que se cree en la base de datos.
    """

    correo = models.EmailField(unique=True, verbose_name="Correo Electrónico")
    nombre = models.CharField(max_length=100, verbose_name="Nombre Completo")
    password = models.CharField(max_length=128, verbose_name="Contraseña")
    is_active = models.BooleanField(default=True, verbose_name="Activo")
    is_staff = models.BooleanField(default=False, verbose_name="Es Staff")

    objects = UsuarioManager()

    # Se usará el correo como campo para la autenticación.
    USERNAME_FIELD = "correo"
    REQUIRED_FIELDS = ["nombre"]

    def __str__(self):
        return self.correo

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

class Archivos(BaseModel):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    filename = models.CharField(max_length=255)
    filepath = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField(default=now)

    class Meta:
        verbose_name = "Archivo"
        verbose_name_plural = "Archivos"
        app_label = settings.APP_NAME

class Prueba(BaseModel):
    fecha = models.DateField()
    numero = models.FloatField()
    texto = models.CharField(max_length= 100)
    texto_grande = models.TextField()
    json = models.JSONField()
    boolean = models.BooleanField()
    fecha_hoy = models.DateTimeField(default=now)
    archivo = models.ManyToManyField(Archivos, through='RelacionArchivos', related_name='pruebas')
    class Meta:
        verbose_name = "Prueba"
        verbose_name_plural = "Pruebas"
        app_label = settings.APP_NAME    
    
class RelacionArchivos(BaseModel):
    id_archivo = models.ForeignKey(Archivos, on_delete=models.CASCADE)
    id_prueba = models.ForeignKey(Prueba, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Relacion Archivos"
        verbose_name_plural = "Relaciones Archivos"   
        unique_together = ('id_archivo', 'id_prueba')
        app_label = settings.APP_NAME