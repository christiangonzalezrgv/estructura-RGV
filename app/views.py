# app/views.py

from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic import TemplateView


class IndexView(TemplateView):
    """
    Vista para la página de inicio.
    """

    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["activeMenu"] = "index"
        return context


class DocumentacionView(TemplateView):
    """
    Vista para la página de documentación.
    """

    template_name = "documentacion.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["activeMenu"] = "documentacion"
        return context


class AuditoriaView(TemplateView):
    """
    Vista para la página de auditoría.
    """

    template_name = "auditoria.html"

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
        # Se puede agregar lógica adicional aquí si se requiere.
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
