from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from ..models import Archivos
#from ..django_models import DynamicModelForm
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from auditlog.models import LogEntry
import json
from django.conf import settings
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
from django.db import transaction



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

def sanitize_data(model, data):
    pass

def upload_file_to_s3_and_save_record(s3_service, archivo, record):
    """
    Sube un archivo a S3 y lo asocia con un registro.
    """
    file_uuid = str(uuid.uuid4())
    filepath = f"{file_uuid}_{archivo.name}"
    s3_service.upload_file(archivo, file_uuid)  # Subir el archivo a S3

    # Guardar la información del archivo en la base de datos
    info_archivo = Archivos(
        id=file_uuid,
        filename=archivo.name,
        filepath=filepath,
    )
    info_archivo.save()
    record.archivo.add(info_archivo)

@login_required
def list_records(request, table_name):
    # Ruta para listar todos los registros de una tabla de forma dinámica.
    model = get_model_by_name(table_name)
    if not model:
        messages.error(request, f"La tabla {table_name} no existe.")
        return HttpResponseRedirect('/')
    
    # Obtener todos los registros, excluyendo 'password'
    fields_to_include = [field.name for field in model._meta.fields if field.name != "password"]
    records = model.objects.values(*fields_to_include)
    
    # Columnas sin 'password'
    columns = fields_to_include
    context = {
        "records": records,
        "columns": columns,
        "table_name": table_name,
        "activeMenu": "bases_de_datos",
        "activeItem": table_name,
        "APP_NAME" : settings.APP_NAME
    }
    return render(request, "dynamic_table.html", context)
    
    #print("Todos los modelos: ",get_all_models())
    #print("Nombre de la tabla", get_model_by_name(table_name))

@login_required
def create_record(request, table_name):
    model = get_model_by_name(table_name)
    if not model:
        messages.error(request, f"La tabla '{table_name}' no existe.")
        return redirect('list_records', table_name=table_name)

    if table_name == f"{settings.APP_NAME}_prueba":
        # Definir el formulario dinámico
        class DynamicModelForm(forms.ModelForm):
            class Meta:
                model = get_model_by_name(table_name)
                exclude = ['fecha_creado', 'fecha_hoy', 'password', 'last_login', 'is_superuser', 'is_active', 'is_staff', 'groups', 'user_permissions']

            archivo = forms.FileField(
                label="Nombre de archivo",
                required=False,
                widget=forms.ClearableFileInput(attrs={'class': 'hidden', 'id': 'file-upload'}),
            )
    else: 
        class DynamicModelForm(forms.ModelForm):
            class Meta:
                model = get_model_by_name(table_name)
                exclude = ['fecha_creado', 'fecha_hoy', 'password', 'last_login', 'is_superuser', 'is_active', 'is_staff', 'groups', 'user_permissions']


    if request.method == 'POST':
        form = DynamicModelForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():  # Usar transacciones para garantizar la integridad
                    new_record = form.save(commit=False)
                    if 'fecha_hoy' in [f.name for f in model._meta.fields]:
                        new_record.fecha_hoy = now()

                    # Guardar el registro
                    new_record.save()

                    # Subir archivos si la tabla lo requiere
                    if table_name == f"{settings.APP_NAME}_prueba":
                        s3_service = S3Service()

                        # Subir múltiples archivos
                        archivos = request.FILES.getlist('archivos[]')
                        for archivo in archivos:
                            if archivo and archivo.name:
                                upload_file_to_s3_and_save_record(s3_service, archivo, new_record)

                        # Subir archivo único
                        archivo = request.FILES.get('archivo')
                        if archivo and archivo.name:
                            upload_file_to_s3_and_save_record(s3_service, archivo, new_record)

                    messages.success(request, "Registro creado exitosamente.")
                    return redirect('list_records', table_name=table_name)

            except Exception as e:
                messages.error(request, f"Error al crear el registro: {str(e)}")
        else:
            messages.error(request, f"Formulario inválido: {form.errors}")
    else:
        form = DynamicModelForm()

    # Agregar opciones para campos FK
    foreign_options = {}
    if table_name == f"{settings.APP_NAME}_ordenes_prueba":
        EmpleadoResponsableModel = get_model_by_name(f"{settings.APP_NAME}_usuario")
        foreign_options["empleado_responsable"] = EmpleadoResponsableModel.objects.all()

    context = {
        "activeMenu": "bases_de_datos",
        "activeItem": table_name,
        "foreign_options": foreign_options,
        "form": form,
        "action": "Crear",
        "table_name": table_name,
        "APP_NAME": settings.APP_NAME,
    }

    return render(request, "dynamic_form.html", context)

@login_required
def edit_record(request, table_name, id):
    pass

@login_required
def datos(request, table_name):
    """
    Endpoint dinámico para retornar datos en formato JSON, con paginación, búsqueda y ordenamiento.
    Se esperan los siguientes parámetros en la query:
    - view: cantidad de registros por página (por defecto 50)
    - search: texto para filtrar registros (por defecto cadena vacía)
    - status: filtro por estado (por defecto "todos")
    - sortField: campo por el que ordenar (por defecto "fecha_creado")
    - sortRule: regla de ordenamiento ("asc" o "desc", por defecto "desc")
    - page: número de página (por defecto 1)
    """

    model = get_model_by_name(table_name)
    if not model:
        messages.error(request, f"La tabla {table_name} no existe.")
        return HttpResponseRedirect('/')
    
    # Obtener parámetros de la consulta
    view = int(request.GET.get("view", 50))
    search = request.GET.get("search", "")
    status = request.GET.get("status", "todos")
    sortField = request.GET.get("sortField", "fecha_creado")
    sortRule = request.GET.get("sortRule", "desc")
    page = int(request.GET.get("page", 1))

    # Iniciar la consulta
    query = model.objects.all()

    # Filtrar por "estatus" si aplica y la columna existe
    if status != "todos" and hasattr(model, 'estatus'):
        query = query.filter(estatus=status)

    # Aplicar búsqueda en columnas de tipo cadena
    if search:
        search_filters = Q()
        for field in model._meta.fields:
            if field.get_internal_type() in ['CharField', 'TextField']:
                search_filters |= Q(**{f"{field.name}__icontains": search})
        query = query.filter(search_filters)

    # Contar el total de registros filtrados
    total = query.count()

    # Aplicar ordenamiento
    if hasattr(model, sortField):
        if sortRule.lower() == "asc":
            query = query.order_by(sortField)
        else:
            query = query.order_by(f"-{sortField}")
    else:
        query = query.order_by('id')

    # Aplicar paginación
    paginator = Paginator(query, view)
    try:
        records = paginator.page(page)
    except EmptyPage:
        records = []

    # Convertir registros a diccionario y pasar todos los campos a str para su visualizacion
    def record_to_dict(record):
        result = {}
        for field in model._meta.fields:
            value = getattr(record, field.name)
            result[field.name] = str(value)
        
        return result

    items = [record_to_dict(record) for record in records]

    # Calcular la cantidad total de páginas
    pages = paginator.num_pages

    return JsonResponse({
        "items": items,
        "total": total,
        "pages": pages,
        "totals": {},  # Puedes incluir totales por estado si lo necesitas
    })
    



@login_required
def eliminar_record(request, table_name, id):
    model = get_model_by_name(table_name)
    if not model:
        messages.error(request, f"La tabla {table_name} no existe.")
        return HttpResponseRedirect('/')

    record = model.objects.get(id=id)
    record.delete()
    messages.success(request, "Registro eliminado exitosamente")
    return HttpResponseRedirect(f'/db/{table_name}')


@login_required
def formulario_record(request, table_name, id):
    model = get_model_by_name(table_name)

    if table_name == f"{settings.APP_NAME}_prueba":
        # Definir el formulario dinámico
        class DynamicModelForm(forms.ModelForm):
            class Meta:
                model = get_model_by_name(table_name)
                exclude = ['fecha_creado', 'fecha_hoy', 'password', 'last_login', 'is_superuser', 'is_active', 'is_staff', 'groups', 'user_permissions']

            archivo = forms.FileField(
                label="Nombre de archivo",
                required=False,
                widget=forms.ClearableFileInput(attrs={'class': 'hidden', 'id': 'file-upload'}),
            )
    else: 
        class DynamicModelForm(forms.ModelForm):
            class Meta:
                model = get_model_by_name(table_name)
                exclude = ['fecha_creado', 'fecha_hoy', 'password', 'last_login', 'is_superuser', 'is_active', 'is_staff', 'groups', 'user_permissions']

    if not model:
        messages.error(request, f"La tabla {table_name} no existe.")
        return HttpResponseRedirect(f'/db/{table_name}')
        
    record = get_object_or_404(model, id=id)
    if not record:
        messages.error(request, f"Registro con ID {id} no encontrado en '{table_name}'.")
        return HttpResponseRedirect(f'/db/{table_name}')

    if request.method == "POST":    
        form = DynamicModelForm(request.POST, instance=record)
        if form.is_valid():
            form.save()
            messages.success(request, "Actualización exitosa.")
            return HttpResponseRedirect(f'/db/{table_name}')
        else:
            messages.error(request, "Error al actualizar. Verifica los datos del formulario.")
    else:
        form = DynamicModelForm(instance=record)

    
    context = {
        "activeMenu": "bases_de_datos",
        "activeItem": table_name,
        "form": form,
        "table_name": table_name,
        "action": "Editar",
        "APP_NAME" : settings.APP_NAME
    }
    return render(request, "dynamic_form.html", context)
    
