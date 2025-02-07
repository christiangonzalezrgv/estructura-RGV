# app/views.py

from django.views.generic import TemplateView


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
