"""
Reportes simplificados.
"""

import os
import sys
from datetime import datetime

_raiz = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _raiz not in sys.path:
    sys.path.insert(0, _raiz)

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle

from logica.dao_paciente import obtener_pacientes, obtener_paciente_por_id
from logica.dao_historia import obtener_historias

_RUTA_REPORTES = os.path.join(_raiz, 'reportes', 'pdf')
os.makedirs(_RUTA_REPORTES, exist_ok=True)

NOMBRE_CLINICA = 'Clínica Odontológica'

def _timestamp():
    return datetime.now().strftime('%Y%m%d_%H%M%S')

def _fecha():
    return datetime.now().strftime('%d/%m/%Y %H:%M')

def _estilos():
    return getSampleStyleSheet()

def generar_ficha_paciente(id_persona):
    paciente = obtener_paciente_por_id(id_persona)
    if not paciente:
        return None

    ruta = os.path.join(_RUTA_REPORTES, f'ficha_paciente_{id_persona}_{_timestamp()}.pdf')
    doc = SimpleDocTemplate(ruta, pagesize=A4)
    styles = _estilos()
    elementos = []

    elementos.append(Paragraph(f"{NOMBRE_CLINICA} - Ficha del Paciente", styles['Title']))
    elementos.append(Paragraph(f"Emitido: {_fecha()}", styles['Normal']))
    elementos.append(Spacer(1, 20))

    datos = [
        ['Cédula:', str(paciente[4])],
        ['Nombre Completo:', f"{paciente[1]} {paciente[2]} {paciente[3]}"],
        ['Edad / Fecha Nac.:', f"{paciente[6]} años / {paciente[5]}"],
        ['Contacto:', f"{paciente[8]} - {paciente[9]}"],
        ['Antecedentes:', str(paciente[7]) if paciente[7] else 'Ninguno']
    ]
    
    tabla = Table(datos, colWidths=[120, 300])
    tabla.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (0,-1), colors.lightgrey),
        ('GRID', (0,0), (-1,-1), 1, colors.black),
        ('PADDING', (0,0), (-1,-1), 6)
    ]))
    
    elementos.append(tabla)
    doc.build(elementos)
    return ruta

def generar_historial_clinico(id_persona):
    paciente = obtener_paciente_por_id(id_persona)
    historias = obtener_historias(id_persona)
    if not paciente:
        return None

    ruta = os.path.join(_RUTA_REPORTES, f'historial_clinico_{id_persona}_{_timestamp()}.pdf')
    doc = SimpleDocTemplate(ruta, pagesize=A4)
    styles = _estilos()
    elementos = []

    elementos.append(Paragraph(f"{NOMBRE_CLINICA} - Historial Clínico", styles['Title']))
    elementos.append(Paragraph(f"Paciente: {paciente[1]} {paciente[2]} {paciente[3]}", styles['Normal']))
    elementos.append(Paragraph(f"Emitido: {_fecha()}", styles['Normal']))
    elementos.append(Spacer(1, 20))

    datos_historia = [['Fecha', 'Motivo', 'Tratamiento']]
    if historias:
        for h in historias:
            datos_historia.append([str(h[2]), str(h[3]), str(h[5])])
    else:
        datos_historia.append(['Sin registros', '', ''])

    tabla = Table(datos_historia, colWidths=[100, 160, 160])
    tabla.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.grey),
        ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
        ('GRID', (0,0), (-1,-1), 1, colors.black),
        ('PADDING', (0,0), (-1,-1), 6)
    ]))
    
    elementos.append(tabla)
    doc.build(elementos)
    return ruta

def generar_directorio_pacientes():
    pacientes = obtener_pacientes()
    ruta = os.path.join(_RUTA_REPORTES, f'directorio_{_timestamp()}.pdf')
    doc = SimpleDocTemplate(ruta, pagesize=landscape(A4))
    styles = _estilos()
    elementos = []

    elementos.append(Paragraph(f"{NOMBRE_CLINICA} - Directorio de Pacientes", styles['Title']))
    elementos.append(Spacer(1, 20))

    datos = [['Cédula', 'Nombre Completo', 'Teléfono', 'Correo']]
    for p in pacientes:
        datos.append([str(p[4]), f"{p[1]} {p[2]} {p[3]}", str(p[9]), str(p[8])])

    tabla = Table(datos)
    tabla.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.grey),
        ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
        ('GRID', (0,0), (-1,-1), 1, colors.black),
        ('PADDING', (0,0), (-1,-1), 6)
    ]))
    
    elementos.append(tabla)
    doc.build(elementos)
    return ruta
