from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from ..models import Usuario
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

@login_required
def Grupos(request):
    usuarios_con_grupos = []
    usuarios = Usuario.objects.all().prefetch_related('groups')  # Optimización con prefetch_related

    for usuario in usuarios:
        grupos = usuario.groups.all()
        usuarios_con_grupos.append({
            'usuario': usuario,
            'grupos': grupos
        })

    context = {
        "usuarios_con_grupos": usuarios_con_grupos  # Agregar usuarios y grupos al contexto
    }
    return render(request, "permisos/grupos.html", context)

    