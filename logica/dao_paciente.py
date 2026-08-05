"""DAO de pacientes: operaciones CRUD sobre la tabla Persona."""

from .base_datos import ConexionBaseDatos
from tkinter import messagebox


def registrar_paciente(paciente):
    """Inserta un nuevo paciente en la base de datos."""
    conexion = ConexionBaseDatos()
    sql = """
        INSERT INTO Persona (
            nombre, apellidoPaterno, apellidoMaterno,
            dni, fechaNacimiento, edad, antecedentes,
            correo, telefono, activo
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 1)
    """
    parametros = (
        paciente.nombre, paciente.apellido_paterno, paciente.apellido_materno,
        paciente.dni, paciente.fecha_nacimiento, paciente.edad,
        paciente.antecedentes, paciente.correo, paciente.telefono
    )
    try:
        conexion.cursor.execute(sql, parametros)
        conexion.cerrar_conexion()
        messagebox.showinfo('Registrar Paciente', 'Paciente registrado exitosamente')
    except Exception:
        messagebox.showerror('Registrar Paciente', 'Error al registrar paciente')


def actualizar_paciente(paciente, id_persona):
    """Actualiza los datos de un paciente existente."""
    conexion = ConexionBaseDatos()
    sql = """
        UPDATE Persona SET
            nombre = ?, apellidoPaterno = ?, apellidoMaterno = ?,
            dni = ?, fechaNacimiento = ?, edad = ?,
            antecedentes = ?, correo = ?, telefono = ?, activo = 1
        WHERE idPersona = ?
    """
    parametros = (
        paciente.nombre, paciente.apellido_paterno, paciente.apellido_materno,
        paciente.dni, paciente.fecha_nacimiento, paciente.edad,
        paciente.antecedentes, paciente.correo, paciente.telefono, id_persona
    )
    try:
        conexion.cursor.execute(sql, parametros)
        conexion.cerrar_conexion()
        messagebox.showinfo('Editar Paciente', 'Paciente editado exitosamente')
    except Exception:
        messagebox.showinfo('Editar Paciente', 'Error al editar paciente')


def dar_baja_paciente(id_persona):
    """Realiza un borrado lógico del paciente (activo = 0)."""
    conexion = ConexionBaseDatos()
    sql = 'UPDATE Persona SET activo = 0 WHERE idPersona = ?'
    try:
        conexion.cursor.execute(sql, (id_persona,))
        conexion.cerrar_conexion()
        messagebox.showinfo('Eliminar Paciente', 'Paciente eliminado exitosamente')
    except Exception:
        messagebox.showwarning('Eliminar Paciente', 'Error al eliminar paciente')


def obtener_pacientes():
    """Retorna la lista de todos los pacientes activos."""
    conexion = ConexionBaseDatos()
    sql = 'SELECT * FROM Persona WHERE activo = 1'
    lista = []
    try:
        conexion.cursor.execute(sql)
        lista = conexion.cursor.fetchall()
        conexion.cerrar_conexion()
    except Exception:
        messagebox.showwarning('Datos', 'Registros no encontrados')
    return lista


def buscar_por_dni(dni):
    """Retorna pacientes cuyo DNI coincide exactamente con el valor dado, incluyendo inactivos."""
    conexion = ConexionBaseDatos()
    sql = 'SELECT * FROM Persona WHERE dni = ?'
    lista = []
    try:
        conexion.cursor.execute(sql, (dni,))
        lista = conexion.cursor.fetchall()
        conexion.cerrar_conexion()
    except Exception:
        messagebox.showwarning('Datos', 'Registros no encontrados')
    return lista


def buscar_por_apellido(apellido):
    """Retorna pacientes cuyo apellido paterno empieza con el texto dado, incluyendo inactivos."""
    conexion = ConexionBaseDatos()
    sql = "SELECT * FROM Persona WHERE apellidoPaterno LIKE ?"
    lista = []
    try:
        conexion.cursor.execute(sql, (f'{apellido}%',))
        lista = conexion.cursor.fetchall()
        conexion.cerrar_conexion()
    except Exception:
        messagebox.showwarning('Datos', 'Registros no encontrados')
    return lista


def obtener_paciente_por_id(id_persona):
    """Retorna la fila completa de un paciente según su ID primario.

    Returns:
        tuple | None: Fila de la base de datos o None si no se encuentra.
    """
    conexion = ConexionBaseDatos()
    sql = 'SELECT * FROM Persona WHERE idPersona = ?'
    resultado = None
    try:
        conexion.cursor.execute(sql, (id_persona,))
        resultado = conexion.cursor.fetchone()
        conexion.cerrar_conexion()
    except Exception:
        messagebox.showwarning('Datos', 'Paciente no encontrado')
    return resultado
