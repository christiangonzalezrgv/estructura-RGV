from django import forms
from .models import *
from django.contrib.auth.models import User, Group

class EmailForm(forms.ModelForm):
    correo = forms.EmailField(
        label="Correo electrónico*",
        max_length=200,
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    class Meta:
        model = Usuario
        fields = ['correo']

class LoginForm(forms.ModelForm):
    correo = forms.EmailField(
        label="Correo electrónico*",
        max_length=50,
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )

    password = forms.CharField(
        label="Contraseña",
        max_length=50,
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Usuario
        fields = ['correo', 'password']

class UsuariosForm(forms.ModelForm):
    nombre = forms.CharField(
        label="Nombre*",
        max_length=50,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    correo = forms.EmailField(
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

    class Meta:
        model = Usuario
        fields = ['nombre','correo', 'is_active']