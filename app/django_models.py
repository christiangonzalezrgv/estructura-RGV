from django import forms
from .models import Usuario
from django.contrib.auth.models import User, Group

class UsuariosForm(forms.ModelForm):
    first_name = forms.CharField(
        label="Nombre*",
        max_length=50,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    username = forms.CharField(
        label="Nombre de usuario*",
        max_length=50,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    email = forms.EmailField(
        label="Correo electrónico*",
        max_length=50,
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    is_active = forms.BooleanField(
        label="Estatus",
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-control'})
    )
    groups = forms.ChoiceField(
        label="Grupo",
        choices=[('prueba_admin', 'prueba_admin'), ('prueba_user', 'prueba_user')],
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Usuario
        fields = ['first_name', 'username','email', 'is_active', 'groups']
    