from django.urls import path
from ..views.views_archivos import (
    list_archivos,
    generate_presigned_url
)

urlpatterns = [
    path("archivos/<id>", list_archivos, name='list_archivos'),
    path("generate-presigned-url", generate_presigned_url, name='generate_presigned_url'),
]
