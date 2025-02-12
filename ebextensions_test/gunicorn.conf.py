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
    """Corrige el acceso a `req.headers` que es una lista de tuplas"""
    headers = dict(req.headers)  # Convierte la lista en un diccionario temporal
    if "CONTENT_LENGTH" not in headers:
        req.headers.append(("CONTENT_LENGTH", "0"))  # Agregar como tupla
