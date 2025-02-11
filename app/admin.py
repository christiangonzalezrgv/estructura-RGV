# app/admin.py
from django.contrib import admin
from .models import *

admin.site.register(LogAuditoria)
admin.site.register(Usuario)