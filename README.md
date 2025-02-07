# Estructura RGV

Estructura base para proyectos Django.

Última actualización: febrero 2025

Versiones utilizadas:

- Python 3.13
- Django 5.1.6

## Estructura

```bash
.
└── estructura-django/
    ├── app/
    │   ├── migrations/
    │   ├── static/
    │   ├── templates/
    │   ├── __init__.py
    │   ├── admin.py
    │   ├── apps.py
    │   ├── models.py
    │   ├── tests.py
    │   ├── urls.py
    │   └── views.py
    ├── config/
    │   ├── __init__.py
    │   ├── asgi.py
    │   ├── settings.py
    │   ├── urls.py
    │   └── wsgi.py
    ├── venv/
    ├── .env
    ├── .gitignore
    ├── manage.py
    └── README.md
```

## Setup inicial

### Entorno virtual

#### Windows

```bash
py -3.13 -m venv venv
venv\Scripts\activate
```

#### Mac

```bash
python -m venv venv
source venv/bin/activate
```

### Dependencias

#### Instalar

```bash
pip install -r requirements.txt
```

#### Actualizar

```bash
pip freeze > requirements.txt
```

### Variables de entorno

Crear un archivo `.env` en la raíz del proyecto con las siguientes variables:

```bash
# Django settings
DEBUG=True
SECRET_KEY=supersecreto123

# Database connection
DATABASE_NAME=mydatabase
DATABASE_USER=myuser
DATABASE_PASSWORD=mypassword
DATABASE_HOST=localhost
DATABASE_PORT=5432
```

### Ejecutar

```bash
python manage.py runserver
```

### Migraciones

```bash
python manage.py makemigrations
python manage.py migrate
```

## Información adicional

### Archivo __init__.py

Este archivo indica que la carpeta es un paquete de Python.

### ¿Qué es ASGI?

ASGI (Asynchronous Server Gateway Interface) es una especificación que describe cómo los servidores web pueden comunicarse con las aplicaciones web, y cómo las aplicaciones web pueden enviar eventos asíncronos a los clientes a través de la conexión HTTP.

### ¿Qué es WSGI?

WSGI (Web Server Gateway Interface) es una especificación que describe cómo un servidor web puede comunicarse con una aplicación web, y cómo la aplicación web puede generar una respuesta HTTP.

### Proyecto y aplicación

#### Proyecto

Un proyecto en Django es la estructura general que maneja toda la configuración y puede contener múltiples aplicaciones. Es el contenedor principal y maneja configuraciones globales como:

- settings.py: Configuración de base de datos, middleware, apps instaladas, etc.
- urls.py: Rutas principales del proyecto.
- wsgi.py / asgi.py: Archivos de configuración para el despliegue.

El proyecto en sí mismo no maneja directamente la lógica de la aplicación; en su lugar, depende de aplicaciones.

#### Aplicación

Las aplicaciones son módulos independientes dentro del proyecto, diseñados para cumplir una función específica. Puedes tener varias aplicaciones en un solo proyecto, por ejemplo:

- usuarios/ → Manejo de autenticación y perfiles.
- productos/ → Gestión de productos en una tienda.
- ventas/ → Manejo de pedidos y transacciones.

### ¿Por qué se crea una carpeta dentro de otra?

Django sigue esta estructura para mantener organizado el código:

1. Carpeta raíz (config/): Es donde puedes agregar otras aplicaciones o archivos de configuración.

2. Segunda carpeta (config/ dentro de la raíz): Es donde están los archivos principales del proyecto. Si Django no hiciera esto, los archivos de configuración (settings.py, urls.py, etc.) quedarían mezclados con archivos de aplicaciones y otros archivos en la raíz, lo que sería desordenado.

### ¿Qué Comandos Puedes Ejecutar con manage.py?

manage.py facilita la ejecución de tareas en Django. Algunos comandos útiles:

- python manage.py runserver: Inicia el servidor de desarrollo en <http://127.0.0.1:8000/>.
- python manage.py migrate: Aplica migraciones pendientes a la base de datos.
- python manage.py makemigrations: Crea nuevas migraciones basadas en los cambios de los modelos.
- python manage.py createsuperuser: Crea un usuario administrador para el panel de Django.
- python manage.py shell: Inicia una consola interactiva de Django.
- python manage.py collectstatic: Recolecta archivos estáticos para producción.
