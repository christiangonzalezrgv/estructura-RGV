# config/urls.py

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("app.urls.urls")),
    path("", include("app.urls.urls_dynamic")),
    path("", include("app.urls.urls_permisos")),
]
