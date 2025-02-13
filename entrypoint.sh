#!/bin/sh
# Ejecuta las migraciones
python manage.py migrate --noinput

# Colecta archivos estáticos
python manage.py collectstatic --noinput

# Inicia Gunicorn para servir la aplicación en el puerto 80
exec gunicorn config.wsgi:application --bind 0.0.0.0:8000
