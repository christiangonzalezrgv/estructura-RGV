from django.urls import path
from ..views.views_permisos import (
    Grupos
)

urlpatterns = [
    path("grupos/lista", Grupos, name="Grupos"),
]