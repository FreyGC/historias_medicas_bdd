"""DAO de historias médicas: operaciones CRUD sobre la tabla historiaMedica."""

from .base_datos import ConexionBaseDatos
from tkinter import messagebox


def obtener_historias(id_persona):
    """Retorna todas las historias médicas del paciente indicado."""
    conexion = ConexionBaseDatos()
    sql = """
        SELECT
            h.idHistoriaMedica,
            p.nombre || ' ' || p.apellidoPaterno || ' ' || p.apellidoMaterno AS nombre_completo,
            h.fechaHistoria,
            h.motivo,
            h.examenAuxiliar,
            h.tratamiento,
            h.detalle
        FROM historiaMedica h
        INNER JOIN Persona p ON p.idPersona = h.idPersona
        WHERE p.idPersona = ?
    """
    lista = []
    try:
        conexion.cursor.execute(sql, (id_persona,))
        lista = conexion.cursor.fetchall()
        conexion.cerrar_conexion()
    except Exception:
        messagebox.showerror('Listar Historia', 'Error al listar historia médica')
    return lista


def registrar_historia(id_persona, fecha_historia, motivo,
                       examen_auxiliar, tratamiento, detalle):
    """Inserta una nueva historia médica en la base de datos."""
    conexion = ConexionBaseDatos()
    sql = """
        INSERT INTO historiaMedica (
            idPersona, fechaHistoria, motivo,
            examenAuxiliar, tratamiento, detalle
        ) VALUES (?, ?, ?, ?, ?, ?)
    """
    parametros = (id_persona, fecha_historia, motivo,
                  examen_auxiliar, tratamiento, detalle)
    try:
        conexion.cursor.execute(sql, parametros)
        conexion.cerrar_conexion()
        messagebox.showinfo('Registro Historia Médica', 'Historia registrada exitosamente')
    except Exception:
        messagebox.showerror('Registro Historia Médica', 'Error al registrar historia')


def borrar_historia(id_historia_medica):
    """Elimina físicamente una historia médica de la base de datos."""
    conexion = ConexionBaseDatos()
    sql = 'DELETE FROM historiaMedica WHERE idHistoriaMedica = ?'
    try:
        conexion.cursor.execute(sql, (id_historia_medica,))
        conexion.cerrar_conexion()
        messagebox.showinfo('Eliminar Historia', 'Historia médica eliminada exitosamente')
    except Exception:
        messagebox.showerror('Eliminar Historia', 'Error al eliminar historia médica')


def actualizar_historia(fecha_historia, motivo, examen_auxiliar,
                        tratamiento, detalle, id_historia_medica):
    """Actualiza los datos de una historia médica existente."""
    conexion = ConexionBaseDatos()
    sql = """
        UPDATE historiaMedica SET
            fechaHistoria = ?, motivo = ?,
            examenAuxiliar = ?, tratamiento = ?, detalle = ?
        WHERE idHistoriaMedica = ?
    """
    parametros = (fecha_historia, motivo, examen_auxiliar,
                  tratamiento, detalle, id_historia_medica)
    try:
        conexion.cursor.execute(sql, parametros)
        conexion.cerrar_conexion()
        messagebox.showinfo('Editar Historia', 'Historia médica editada exitosamente')
    except Exception:
        messagebox.showerror('Editar Historia', 'Error al editar historia médica')
