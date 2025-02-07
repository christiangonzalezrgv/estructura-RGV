# app/views.py

from django.views.generic import TemplateView


from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy


class IndexView(TemplateView):
    """Página de inicio"""

    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["activeMenu"] = "index"
        return context


class DocumentacionView(TemplateView):
    """Página de documentación"""

    template_name = "documentacion.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["activeMenu"] = "documentacion"
        return context


class AuditoriaView(TemplateView):
    """Página de auditoría"""

    template_name = "auditoria.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["activeMenu"] = "auditoria"
        return context


class UserLoginView(LoginView):
    """
    Vista para el login de usuarios.
    Se utiliza la plantilla personalizada 'auth/login.html'.

    Nota:
    - redirect_authenticated_user: redirecciona automáticamente a un usuario ya autenticado.
    - success_url: URL a la que se redirecciona si el login es exitoso.
    """

    template_name = "auth/login.html"
    redirect_authenticated_user = True
    success_url = reverse_lazy("index")

    def form_valid(self, form):
        """
        Si el formulario de login es válido, se procede a autenticar y redirigir al usuario.
        Aquí se puede agregar lógica adicional si es necesario.
        """
        
        return super().form_valid(form)
