# app/views.py

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView


class DashboardView(LoginRequiredMixin, TemplateView):
    """
    Vista para el dashboard principal. Se requiere autenticación.
    """

    template_name = "index.html"
