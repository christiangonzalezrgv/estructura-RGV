from django import forms
from .models import Usuario
from django.contrib.auth.models import User, Group

class DynamicModelForm(forms.ModelForm):
        nombre = forms.CharField(
        label="Nombre completo",
        max_length=50,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-input h-10'})
        )
        correo = forms.EmailField(
        label="Correo electrónico",
        max_length=50,
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-input h-10'})
        )
        class Meta:
            model = Usuario
            exclude = ['fecha_creado', 'password', 'last_login', 'is_superuser', 'is_active', 'is_staff', 'groups', 'user_permissions'] 