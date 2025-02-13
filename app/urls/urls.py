# app/urls.py

from django.contrib.auth.views import LogoutView
from django.urls import path

from ..views.views import (
    AuditoriaView,
    DocumentacionView,
    ForgotPasswordView,
    HealthCheckView,
    IndexView,
    UserLoginView,
    api_prueba,
)

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("api/prueba", api_prueba, name='api_prueba'),
    path("api/prueba/<num>", api_prueba, name='api_prueba'),
    path("documentacion/", DocumentacionView.as_view(), name="documentacion"),
    path("auditoria/", AuditoriaView.as_view(), name="auditoria"),
    path("auth/login/", UserLoginView.as_view(), name="login"),
    path("auth/logout/", LogoutView.as_view(next_page="login"), name="logout"),
    path("auth/forgotpassword/", ForgotPasswordView.as_view(), name="forgotpassword"),
    path("health/", HealthCheckView.as_view(), name="health"),
]
