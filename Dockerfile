# Usa una imagen base con Python 3.13
FROM python:3.13-slim

# Evita la generación de archivos .pyc y configura salida sin búfer
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Define el directorio de trabajo
WORKDIR /app

# Copia el archivo de dependencias, actualiza pip e instala las dependencias
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copia el resto del código de la aplicación
COPY . /app/

# Ejecuta collectstatic para recopilar archivos estáticos en STATIC_ROOT
RUN python manage.py collectstatic --noinput

# Da permisos de ejecución al entrypoint.sh
RUN chmod +x entrypoint.sh

# Expone el puerto 80 (el que usará Gunicorn)
EXPOSE 80

# Define el entrypoint para el contenedor
ENTRYPOINT ["./entrypoint.sh"]
