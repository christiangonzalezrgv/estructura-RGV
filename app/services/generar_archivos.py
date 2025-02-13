# /servicios/generar_archivos.py

import io
import pandas as pd
from django.db import connection
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle
from reportlab.graphics import renderPDF
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF
from django.conf import settings
from xml.sax.saxutils import escape



class GenerarExcelService:
    @staticmethod
    def generar_excel(nombre_tabla):
        try:
            with connection.cursor() as cursor:
                # Obtener las columnas de la tabla
                cursor.execute(f"SELECT column_name, data_type FROM information_schema.columns WHERE table_name = '{nombre_tabla}'")
                columns_info = cursor.fetchall()

                # Construir una lista de columnas con manejo de timezone
                columns = []
                for column_name, data_type in columns_info:
                    if data_type == "timestamp with time zone":
                        # Convertir timestamptz a naive timestamp
                        columns.append(f"{column_name} AT TIME ZONE 'UTC' AS {column_name}")
                    else:
                        columns.append(column_name)

                # Construir la consulta SQL final
                query = f"SELECT {', '.join(columns)} FROM {nombre_tabla}"
                cursor.execute(query)
                columns = [col[0] for col in cursor.description]
                rows = cursor.fetchall()
                
            df = pd.DataFrame(rows, columns=columns)

            #Truncamos el nombre de la tabla por si excede los 31 caracteres permitidos para el nombre del archivo.
            nombre_tabla = nombre_tabla[:30]
            # Exportar a un archivo Excel
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
                df.to_excel(writer, index=False, sheet_name=nombre_tabla)

            output.seek(0)
            return output.getvalue(), None
        except Exception as e:
            return None, str(e)


class GenerarPDFService:
    @staticmethod
    def generar_pdf(nombre_tabla, registro_id):
        try:
            if not nombre_tabla.isidentifier():
                return None, f"El nombre de la tabla '{nombre_tabla}' no es válido."

            # Ejecutar consulta SQL segura usando Django
            with connection.cursor() as cursor:
                cursor.execute(
                    f"SELECT * FROM {nombre_tabla} WHERE id = %s", [registro_id]
                )
                columnas = [col[0] for col in cursor.description]
                fila = cursor.fetchone()

            if not fila:
                return (
                    None,
                    f"No se encontró el registro con ID {registro_id} en la tabla {nombre_tabla}.",
                )

            registro = dict(zip(columnas, fila))

            # Crear PDF
            buffer = io.BytesIO()
            doc = SimpleDocTemplate(buffer, pagesize=letter)

            # Estilos
            styles = getSampleStyleSheet()
            title_style = ParagraphStyle(
                name="Title",
                fontSize=16,
                leading=20,
                alignment=TA_LEFT,
                textColor=colors.black,
            )
            cell_style = ParagraphStyle(
                name="Cell",
                fontSize=10,
                leading=12,
                alignment=TA_LEFT,
                wordWrap=True,
            )

            # Elementos iniciales
            elements = []

            # Ruta del logo
            logo_path = "estructura_django/static/images/template/logo-light.svg"
            drawing = svg2rlg(logo_path)

            # Header con logo y título
            def draw_header(canvas, doc):
                canvas.saveState()

                # Posición y escala del logo
                logo_x = 50
                logo_y = 720
                logo_scale = 1

                # Escalar y dibujar el logo
                canvas.saveState()
                canvas.translate(logo_x, logo_y)
                canvas.scale(logo_scale, logo_scale)
                drawing.width, drawing.height = 100, 100
                renderPDF.draw(drawing, canvas, 0, 0)
                canvas.restoreState()

                # Título
                title_y = logo_y - 60
                canvas.setFont("Helvetica-Bold", 16)
                canvas.drawString(
                    50, title_y, f"Datos de la tabla: {nombre_tabla.replace('_', ' ')}"
                )

                canvas.restoreState()

            # Espaciado para separar la tabla del encabezado
            elements.append(Spacer(1, 100))

            # Tabla
            data = [["Campo", "Valor"]]
            for campo, valor in registro.items():
                # Convertir valor a cadena y manejar valores nulos
                valor = str(valor) if valor is not None else "N/A"
                # Escapar caracteres especiales para evitar errores en Paragraph
                campo = escape(campo)
                valor = escape(valor)
                data.append(
                    [Paragraph(campo, cell_style), Paragraph(valor, cell_style)]
                )

            table = Table(data, colWidths=[150, 350])
            table.setStyle(
                TableStyle(
                    [
                        ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
                        ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),
                        ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                        ("FONTSIZE", (0, 0), (-1, 0), 12),
                        ("BOTTOMPADDING", (0, 0), (-1, 0), 8),
                        ("BACKGROUND", (0, 1), (-1, -1), colors.whitesmoke),
                        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                        ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ]
                )
            )

            elements.append(table)

            # Generar PDF con header
            doc.build(elements, onFirstPage=draw_header)
            buffer.seek(0)
            return buffer.getvalue(), None

        except Exception as e:
            return None, str(e)
