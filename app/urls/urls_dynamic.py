from django.urls import path
from ..views.views_dynamic import (
    list_records,
    create_record,
    edit_record,
    datos,
    eliminar_record,
    formulario_record,
)

urlpatterns = [
    path("db/<table_name>", list_records, name="list_records"),
    path("db/<table_name>/create", create_record, name="create_record"),
    path("db/<table_name>/edit/<id>", edit_record, name="login"),
    path("db/<table_name>/datos", datos, name="datos"),
    path("db/<table_name>/eliminar/<id>", eliminar_record, name="eliminar_record"),
    path("db/<table_name>/formulario/<id>", formulario_record, name="formulario_record"),
]
