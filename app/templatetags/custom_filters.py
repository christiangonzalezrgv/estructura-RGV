from django import template

register = template.Library()

@register.filter
def field_type(field):
    """
    Devuelve el nombre de la clase del campo.
    """
    return field.field.__class__.__name__

@register.filter
def format_name(value):
    """
    Reemplaza guiones bajos por espacios.
    """
    value = value.replace("nombre_app_", " ")
    value = value.replace("django_", " ")
    value = value.replace("auth_", " ")
    return value.replace("_", " ")

@register.filter
def dictlookup(dictionary, key):
    return dictionary.get(key, "-")