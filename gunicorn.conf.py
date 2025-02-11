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
    """Evita que Gunicorn falle si `CONTENT_LENGTH` no está presente"""
    if "CONTENT_LENGTH" not in req.headers:
        req.headers["CONTENT_LENGTH"] = "0"
