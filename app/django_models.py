from django import forms
from .models import Usuario
from django.contrib.auth.models import User, Group

class EmailForm(forms.Form):
    correo = forms.EmailField(
        label="Correo",
        max_length=200,
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )