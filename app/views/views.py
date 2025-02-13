# app/views.py

from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView
from django.db import connection
from ..models import Prueba
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from ..services.send_email import forgot_password_email
import string
import secrets
from django.http import HttpResponseRedirect
from django.contrib import messages
from ..models import Usuario
from ..django_models import EmailForm
from django.shortcuts import render





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
    Maneja el envío del formulario para generar una nueva contraseña.
    """

    template_name = "auth/forgotpassword.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["activeMenu"] = "forgotpassword"
        context["form"] = EmailForm()  # Añade el formulario al contexto
        return context

    def post(self, request, *args, **kwargs):
        """
        Maneja el envío del formulario para generar una nueva contraseña.
        """
        try:
            form = EmailForm(request.POST)
            if form.is_valid():
                correo_electronico = form.cleaned_data["correo"]
                usuario = Usuario.objects.filter(correo=correo_electronico).first()
                if usuario:
                    # Genera una nueva contraseña aleatoria
                    alfabeto = string.ascii_letters + string.digits
                    contrasena = ''.join(secrets.choice(alfabeto) for i in range(20))
                    
                    # Envía el correo electrónico con la nueva contraseña
                    forgot_password_email(correo_electronico, contrasena)
                    
                    # Actualiza la contraseña del usuario en la base de datos
                    usuario.set_password(contrasena)  # Hashea la contraseña
                    usuario.save()
                    
                    # Mensaje de éxito y redirección
                    messages.success(request, "Se ha enviado un correo electrónico con tu nueva contraseña.")
                    return HttpResponseRedirect('/auth/login/')
                else:
                    # Mensaje de error si el correo no existe
                    messages.error(request, "Correo electrónico es incorrecto. Inténtalo nuevamente.")
                    return render(request, self.template_name, {"form": form})
            else:
                # Mensaje de error si el formulario no es válido
                print(form.errors)
                messages.error(request, "Error al generar contraseña. Verifica los datos ingresados.")
                return render(request, self.template_name, {"form": form})
        except Exception as e:
            # Mensaje de error en caso de excepción
            messages.error(request, f"Error al enviar la contraseña: {e}")
            return HttpResponseRedirect('/auth/login/')

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


class HealthCheckView(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse("OK", status=200)