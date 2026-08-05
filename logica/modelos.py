"""Modelos de dominio del sistema de historias médicas."""


class Persona:
    """Representa a un paciente registrado en el sistema."""

    def __init__(self, nombre, apellido_paterno, apellido_materno, dni,
                 fecha_nacimiento, edad, antecedentes, correo, telefono):
        self.id_persona = None
        self.nombre = nombre
        self.apellido_paterno = apellido_paterno
        self.apellido_materno = apellido_materno
        self.dni = dni
        self.fecha_nacimiento = fecha_nacimiento
        self.edad = edad
        self.antecedentes = antecedentes
        self.correo = correo
        self.telefono = telefono

    def __str__(self):
        return (
            f'Persona[{self.nombre}, {self.apellido_paterno}, '
            f'{self.apellido_materno}, {self.dni}, {self.fecha_nacimiento}, '
            f'{self.edad}, {self.antecedentes}, {self.correo}, {self.telefono}]'
        )


class HistoriaMedica:
    """Representa un registro de historia médica asociado a un paciente."""

    def __init__(self, id_persona, fecha_historia, motivo,
                 examen_auxiliar, tratamiento, detalle):
        self.id_historia_medica = None
        self.id_persona = id_persona
        self.fecha_historia = fecha_historia
        self.motivo = motivo
        self.examen_auxiliar = examen_auxiliar
        self.tratamiento = tratamiento
        self.detalle = detalle

    def __str__(self):
        return (
            f'HistoriaMedica[{self.id_persona}, {self.fecha_historia}, '
            f'{self.motivo}, {self.examen_auxiliar}, {self.tratamiento}, '
            f'{self.detalle}]'
        )
