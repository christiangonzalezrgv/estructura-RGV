# app/urls.py

from django.contrib.auth.views import LogoutView
from django.urls import path

from .views import AuditoriaView, DocumentacionView, IndexView, UserLoginView

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("documentacion/", DocumentacionView.as_view(), name="documentacion"),
    path("auditoria/", AuditoriaView.as_view(), name="auditoria"),
    # Ruta para el login
    path("auth/login/", UserLoginView.as_view(), name="login"),
    # Ruta para el logout
    path("auth/logout/", LogoutView.as_view(), name="logout"),
    # implementar forgot password
]
