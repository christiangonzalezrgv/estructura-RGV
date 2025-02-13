from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from ..models import Archivos, RelacionArchivos
#from ..django_models import DynamicModelForm
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from auditlog.models import LogEntry
import json
from django.apps import apps
from django.db import models
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage
from django.utils.dateformat import format as date_format
from django.utils.timezone import now
from django import forms
from django.conf import settings
import uuid 
from app.services.boto3_s3 import S3Service
from django.db import connection
from django.views.decorators.csrf import csrf_exempt


def get_all_models():
    """
    Retorna una lista de todos los modelos registrados en Django
    que están asociados a una tabla en la base de datos.
    """
    all_models = []
    for model in apps.get_models():
        if isinstance(model._meta, models.options.Options) and model._meta.db_table:
            all_models.append(model)
    #for model in all_models:
        #print(model._meta.db_table)
    return all_models

def get_model_by_name(table_name):
    """
    Retorna el modelo que corresponde al nombre de la tabla proporcionado.
    Si no se encuentra, retorna None.
    """
    for model in get_all_models():
        if model._meta.db_table == table_name:
            return model
    return None

@login_required
def list_archivos(request, id):
    try:
        records = Archivos.objects.filter(
            relacionarchivos__id_prueba_id=id
        ).values('filename', 'filepath', 'uploaded_at')
        
        # Si no hay registros, mostrar un mensaje
        if not records:
            print("No se encontraron archivos para la prueba")
            messages.info(request, f"No se encontraron archivos para la prueba con ID {id}.")
            return HttpResponseRedirect('/')
        
        print(records)
        # Contexto para la plantilla
        context = {
            "records": records,
            "columns": ['filename', 'filepath', 'uploaded_at'],
            "table_name": "archivos",
            "activeMenu": "bases_de_datos",
            "activeItem": "archivos",
            "id": id
        }
        return render(request, "archivos.html", context)
    
    except Exception as e:
        # Manejar errores en la ejecución del query
        print("Error al obtener los archivos:")
        messages.error(request, f"Error al obtener los archivos: {e}")
        return HttpResponseRedirect('/')

@csrf_exempt  # Desactiva la protección CSRF para esta vista (útil para APIs)
def generate_presigned_url(request):
    """
    Genera y retorna una URL firmada para descargar un archivo de S3.
    """
    try:
        s3_service = S3Service()
        import json
        # Obtener el JSON del cuerpo de la solicitud
        data = json.loads(request.body)
        filepath = data.get("filepath")

        # Validar que el campo 'filepath' esté presente
        if not filepath:
            return JsonResponse({"error": "El campo 'filepath' es obligatorio"}, status=400)

        # Generar la URL firmada usando el servicio de S3
        presigned_url = s3_service.generate_presigned_url(filepath)

        # Retornar la URL firmada en la respuesta
        return JsonResponse({"presigned_url": presigned_url}, status=200)

    except Exception as e:
        # Manejar errores y retornar un mensaje de error
        return JsonResponse({"error": str(e)}, status=500)