# python/services/send_email.py

import smtplib
from django.template.loader import render_to_string
import os

def send_html_email(subject, recipient_email, template, sender_name="Empresa", **kwargs):
    EMAIL_USUARIO = os.environ.get('EMAIL_USUARIO')
    EMAIL_CONTRASENA = os.environ.get('EMAIL_CONTRASENA')
    try:
        # Conexión con el servidor SMTP
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()

            # Verificar si las variables de entorno están correctamente cargadas
            if not EMAIL_USUARIO or not EMAIL_CONTRASENA:
                raise Exception(
                    "Las credenciales de correo no están configuradas correctamente."
                )

            # Iniciar sesión en la cuenta de correo
            server.login(EMAIL_USUARIO, EMAIL_CONTRASENA)

            # Renderizar la plantilla HTML con los datos
            html_content = render_to_string(template, kwargs)

            # Construir el mensaje de correo
            from_email = f"{sender_name} <{EMAIL_USUARIO}>"
            message = f"Subject: {subject}\nFrom: {from_email}\nTo: {recipient_email}\nContent-Type: text/html\n\n{html_content}".encode(
                "utf-8"
            )

            # Enviar el correo
            server.sendmail(EMAIL_USUARIO, recipient_email, message)

    except smtplib.SMTPException as smtp_error:
        # Capturar errores específicos de SMTP
        raise Exception(f"Error SMTP al enviar el correo: {smtp_error}")

    except Exception as e:
        # Capturar cualquier otro error
        raise Exception(f"Error general al enviar el correo: {e}")


def send_email(recipient_email, name, code,id_encuesta,centro_de_salud):
    try:
        # Enviar correo al cliente
        send_html_email(
            subject="Aplicación",
            recipient_email=recipient_email,
            template="partials/email_template.html",
            name=name,
            body_content="Acabas de crear una nueva encuesta de Aplicación.",
            details_list=[
                f"Centro de Salud: {centro_de_salud}",
                f"ID Encuesta: {id_encuesta}",
                f"Código de seguridad: {code}"
            ]
        )
    except Exception as e:
        raise Exception(f"Error al enviar correos: {e}")

def forgot_password_email(recipient_email,contrasena):
    try:
        # Enviar correo al cliente
        send_html_email(
            subject="Nuevo contraseña - Aplicación",
            recipient_email=recipient_email,
            template="partials/email_template.html",
            body_content="Se acaba de crear una nueva contraseña para tu correo electrónico",
            details_list=[
                f"Nueva contraseña: {contrasena}"
            ]
        )
    except Exception as e:
        raise Exception(f"Error al enviar correos: {e}")