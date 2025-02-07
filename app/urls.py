# app/urls.py

from django.urls import path

from .views import AuditoriaView, DocumentacionView, IndexView

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("documentacion/", DocumentacionView.as_view(), name="documentacion"),
    path("auditoria/", AuditoriaView.as_view(), name="auditoria"),
]
