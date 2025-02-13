# app/views.py

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.conf import settings
from django.db import connection
from ..models import Prueba  # Asegúrate de importar tu modelo Prueba
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse


class IndexView(LoginRequiredMixin, TemplateView):
    """
    Vista para la página de inicio protegida.
    """

    template_name = "index.html"  # Asegúrate de que este sea el path correcto
    login_url = reverse_lazy("login")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["activeMenu"] = "index"

        # Leer el archivo SQL y ejecutar la consulta
        with open('app/static/sql/paneles.sql', 'r', encoding='utf-8') as file:
            sql_query = file.read()

        with connection.cursor() as cursor:
            cursor.execute(sql_query)
            paneles = cursor.fetchone()

        # Obtener las opciones de la base de datos
        opciones = (
            Prueba.objects.values_list('numero', flat=True)
            .distinct()
            .order_by('numero')
        )

        # Agregar los datos al contexto
        context['paneles'] = paneles
        context['opciones'] = opciones

        return context

class DocumentacionView(LoginRequiredMixin, TemplateView):
    """
    Vista para la página de documentación protegida.
    """

    template_name = "documentacion.html"
    login_url = reverse_lazy("login")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["activeMenu"] = "documentacion"
        return context


class AuditoriaView(LoginRequiredMixin, TemplateView):
    """
    Vista para la página de auditoría protegida.
    """

    template_name = "auditoria.html"
    login_url = reverse_lazy("login")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["activeMenu"] = "auditoria"
        return context


class UserLoginView(LoginView):
    """
    Vista para el login de usuarios.
    Se utiliza la plantilla 'auth/login.html'.
    """

    template_name = "auth/login.html"
    redirect_authenticated_user = True
    success_url = reverse_lazy("index")

    def form_valid(self, form):
        return super().form_valid(form)


class ForgotPasswordView(TemplateView):
    """
    Vista para la página de "Olvidé mi contraseña".
    Por el momento, solo renderiza el template sin lógica adicional.
    """

    template_name = "auth/forgotpassword.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["activeMenu"] = "forgotpassword"
        return context
    
@login_required
def api_prueba(request, num=None):
    numero = num
    params = []

    with open('app/static/sql/prueba.sql', 'r', encoding='utf-8') as file:
        sql_query = file.read()
    
    # Si el parámetro no es "todos", agrega la condición
    if numero != 'todos':
        sql_query += " AND numero = %s"
        params.append(numero)

    # Agregar agrupación al final de la consulta
    sql_query += """
    group by TO_CHAR(fecha_hoy::DATE, 'YYYY-MM-DD')
    """

    # Ejecuta la consulta en la base de datos
    with connection.cursor() as cursor:
        cursor.execute(sql_query, params)
        columns = [col[0] for col in cursor.description]
        results = [
            dict(zip(columns, row))
            for row in cursor.fetchall()
        ]

    return JsonResponse(results, safe=False)