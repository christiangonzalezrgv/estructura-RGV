# app/views.py

from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView


class IndexView(LoginRequiredMixin, TemplateView):
    """
    Vista para la página de inicio protegida.
    """

    template_name = "index.html"
    login_url = reverse_lazy("login")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["activeMenu"] = "index"
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


class HealthCheckView(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse("OK", status=200)
