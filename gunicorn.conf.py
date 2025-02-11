import os

workers = 4
bind = "0.0.0.0:8000"
accesslog = "-"  # Muestra los logs de acceso en la consola
errorlog = "-"   # Muestra los logs de errores en la consola
loglevel = "info"
timeout = 120  # Aumenta el tiempo de espera
graceful_timeout = 120
keepalive = 5

def pre_request(worker, req):
    """Evita errores cuando `CONTENT_LENGTH` no está definido"""
    content_length = req.headers.get("CONTENT_LENGTH")
    if content_length is None:
        req.headers.append(("CONTENT_LENGTH", "0"))  # Agregar como tupla en lugar de diccionario
