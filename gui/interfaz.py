import os
import sys
from tkcalendar import *
_directorio_base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(_directorio_base)
if _directorio_base not in sys.path:
    sys.path.append(_directorio_base)

import tkinter as tk
from tkinter import ttk, Toplevel, messagebox
import tkcalendar as tc
from datetime import datetime, date
import re

from logica.modelos import Persona
from logica.dao_paciente import (
    registrar_paciente, actualizar_paciente, dar_baja_paciente,
    obtener_pacientes, buscar_por_dni, buscar_por_apellido
)
from logica.dao_historia import (
    obtener_historias, registrar_historia, borrar_historia, actualizar_historia
)
from gui.constantes import (
    COLOR_FONDO, COLOR_SUPERFICIE, COLOR_TEXTO, COLOR_TEXTO_BTN,
    COLOR_BTN_NUEVO, COLOR_BTN_NUEVO_ACT,
    COLOR_BTN_GUARDAR, COLOR_BTN_GUARDAR_ACT,
    COLOR_BTN_CANCELAR, COLOR_BTN_CANCELAR_ACT,
    COLOR_BTN_EDITAR, COLOR_BTN_EDITAR_ACT,
    COLOR_BTN_BUSCAR, COLOR_BTN_BUSCAR_ACT,
    COLOR_BTN_LIMPIAR, COLOR_BTN_LIMPIAR_ACT,
    COLOR_BTN_CALENDARIO, COLOR_BTN_CALENDARIO_ACT,
    COLOR_BTN_HISTORIAL, COLOR_BTN_HISTORIAL_ACT,
    COLOR_BTN_PELIGRO, COLOR_BTN_PELIGRO_ACT,
    COLOR_FILA_PAR, COLOR_SELECCIONADO,
    FUENTE_ETIQUETA, FUENTE_ENTRADA, FUENTE_BTN,
)
from reportes.generador_pdf import (
    generar_ficha_paciente,
    generar_historial_clinico,
    generar_directorio_pacientes,
)


class MarcoSistema(tk.Frame):

    def __init__(self, raiz):
        super().__init__(raiz, width=1280, height=720)
        self.raiz = raiz
        self.pack()
        self.config(bg=COLOR_FONDO)

        self.id_persona = None
        self.id_persona_historia = None
        self.id_historia_medica = None
        self.id_historia_medica_editar = None

        self._configurar_estilo()
        self._crear_barra_menu()
        self.crear_campos_paciente()
        self.deshabilitar_formulario()
        self.cargar_tabla_pacientes()

    # Barra de menú
    def _crear_barra_menu(self):
        """Barra de menú con el menú desplegable 'Reportes'."""
        barra = tk.Menu(
            self.raiz,
            bg='#1A1C30',
            fg='#D8DCF0',
            activebackground='#2F52CC',
            activeforeground='#FFFFFF',
            font=('Segoe UI', 10),
            relief='flat',
            bd=0,
        )
        self.raiz.config(menu=barra)

        menu_reportes = tk.Menu(
            barra,
            tearoff=0,
            bg='#14162A',
            fg='#D8DCF0',
            activebackground='#2F52CC',
            activeforeground='#FFFFFF',
            font=('Segoe UI', 10),
            relief='flat',
            bd=1,
        )
        barra.add_cascade(label='  📄 Reportes  ', menu=menu_reportes)

        menu_reportes.add_command(
            label='  🗂  Ficha Resumen del Paciente',
            command=self._reporte_ficha,
        )
        menu_reportes.add_command(
            label='  📋  Historial Clínico Completo',
            command=self._reporte_historial,
        )
        menu_reportes.add_separator()
        menu_reportes.add_command(
            label='  📇  Directorio de Pacientes',
            command=self._reporte_directorio,
        )

    #Callbacks de reportes
    def _reporte_ficha(self):
        """Genera la Ficha Resumen PDF del paciente seleccionado."""
        try:
            id_sel = self.tabla_pacientes.item(
                self.tabla_pacientes.selection()
            )['text']
            if not id_sel:
                messagebox.showwarning(
                    'Reportes', 'Selecciona un paciente en la tabla primero.'
                )
                return
        except Exception:
            messagebox.showwarning(
                'Reportes', 'Selecciona un paciente en la tabla primero.'
            )
            return

        try:
            ruta = generar_ficha_paciente(id_sel)
            if ruta:
                messagebox.showinfo(
                    'Reporte generado',
                    f'Ficha Resumen generada exitosamente.\n\n{ruta}'
                )
                os.startfile(ruta)
            else:
                messagebox.showerror('Reportes', 'No se pudo generar la ficha.')
        except Exception as e:
            messagebox.showerror('Reportes', f'Error al generar reporte:\n{e}')

    def _reporte_historial(self):
        """Genera el Historial Clínico Completo PDF del paciente seleccionado."""
        try:
            id_sel = self.tabla_pacientes.item(
                self.tabla_pacientes.selection()
            )['text']
            if not id_sel:
                messagebox.showwarning(
                    'Reportes', 'Selecciona un paciente en la tabla primero.'
                )
                return
        except Exception:
            messagebox.showwarning(
                'Reportes', 'Selecciona un paciente en la tabla primero.'
            )
            return

        try:
            ruta = generar_historial_clinico(id_sel)
            if ruta:
                messagebox.showinfo(
                    'Reporte generado',
                    f'Historial Clínico generado exitosamente.\n\n{ruta}'
                )
                os.startfile(ruta)
            else:
                messagebox.showerror('Reportes', 'No se pudo generar el historial.')
        except Exception as e:
            messagebox.showerror('Reportes', f'Error al generar reporte:\n{e}')

    def _reporte_directorio(self):
        """Genera el Directorio de Pacientes PDF en formato apaisado."""
        try:
            ruta = generar_directorio_pacientes()
            if ruta:
                messagebox.showinfo(
                    'Reporte generado',
                    f'Directorio de Pacientes generado exitosamente.\n\n{ruta}'
                )
                os.startfile(ruta)
            else:
                messagebox.showerror('Reportes', 'No se pudo generar el directorio.')
        except Exception as e:
            messagebox.showerror('Reportes', f'Error al generar reporte:\n{e}')

    # ── Configuración inicial ────────────────────────────────────────────────

    def _configurar_estilo(self):
        """Aplica el tema visual a los componentes Treeview."""
        estilo = ttk.Style()
        estilo.theme_use('clam')
        estilo.configure(
            'Treeview',
            background=COLOR_SUPERFICIE,
            foreground=COLOR_TEXTO,
            fieldbackground=COLOR_SUPERFICIE,
            rowheight=24,
            borderwidth=0,
            font=('Segoe UI', 11),
        )
        estilo.map(
            'Treeview',
            background=[('selected', COLOR_SELECCIONADO)],
            foreground=[('selected', '#FFFFFF')],
        )
        estilo.configure(
            'Treeview.Heading',
            background='#1A1C30',
            foreground='#8892A0',
            font=('Segoe UI', 10, 'bold'),
            borderwidth=0,
            relief='flat',
        )

    # ── Formulario de paciente ───────────────────────────────────────────────

    def crear_campos_paciente(self):
        """Crea las etiquetas, campos de entrada y botones del formulario de paciente."""
        # Etiquetas del formulario
        definicion_etiquetas = [
            ('Nombre:', 0), ('Apellido Paterno:', 1), ('Apellido Materno:', 2),
            ('DNI:', 3), ('Fecha Nacimiento:', 4), ('Edad:', 5),
            ('Antecedentes:', 6), ('Correo:', 7), ('Teléfono:', 8),
        ]
        for texto, fila in definicion_etiquetas:
            tk.Label(
                self, text=texto, font=FUENTE_ETIQUETA,
                bg=COLOR_FONDO, fg=COLOR_TEXTO
            ).grid(column=0, row=fila, padx=10, pady=5)

        # Variables de los campos de entrada
        self.var_nombre            = tk.StringVar()
        self.var_apellido_paterno  = tk.StringVar()
        self.var_apellido_materno  = tk.StringVar()
        self.var_dni               = tk.StringVar()
        self.var_fecha_nacimiento  = tk.StringVar()
        self.var_edad              = tk.StringVar()
        self.var_antecedentes      = tk.StringVar()
        self.var_correo            = tk.StringVar()
        self.var_telefono          = tk.StringVar()

        variables_formulario = [
            self.var_nombre, self.var_apellido_paterno, self.var_apellido_materno,
            self.var_dni, self.var_fecha_nacimiento, self.var_edad,
            self.var_antecedentes, self.var_correo, self.var_telefono,
        ]

        # Crear entradas y almacenarlas en lista para habilitar/deshabilitar en bloque
        self._entradas_formulario = []
        for variable, fila in zip(variables_formulario, range(9)):
            entrada = tk.Entry(
                self, textvariable=variable, width=50,
                font=FUENTE_ENTRADA, bg=COLOR_SUPERFICIE,
                fg=COLOR_TEXTO, insertbackground=COLOR_TEXTO,
            )
            entrada.grid(column=1, row=fila, padx=10, pady=5, columnspan=2)
            self._entradas_formulario.append(entrada)

        # Referencias directas para insertar valores al editar
        (self.entrada_nombre, self.entrada_apellido_paterno,
         self.entrada_apellido_materno, self.entrada_dni,
         self.entrada_fecha_nacimiento, self.entrada_edad,
         self.entrada_antecedentes, self.entrada_correo,
         self.entrada_telefono) = self._entradas_formulario

        # Botones de acción del formulario
        self.boton_nuevo = tk.Button(
            self, text='Nuevo', command=self.habilitar_formulario,
            width=20, font=FUENTE_BTN, fg=COLOR_TEXTO_BTN,
            bg=COLOR_BTN_NUEVO, cursor='hand2',
            activebackground=COLOR_BTN_NUEVO_ACT,
        )
        self.boton_nuevo.grid(column=0, row=9, padx=10, pady=5)

        self.boton_guardar = tk.Button(
            self, text='Guardar', command=self.guardar_paciente,
            width=20, font=FUENTE_BTN, fg=COLOR_TEXTO_BTN,
            bg=COLOR_BTN_GUARDAR, cursor='hand2',
            activebackground=COLOR_BTN_GUARDAR_ACT,
        )
        self.boton_guardar.grid(column=1, row=9, padx=10, pady=5)

        self.boton_cancelar = tk.Button(
            self, text='Cancelar', command=self.deshabilitar_formulario,
            width=20, font=FUENTE_BTN, fg=COLOR_TEXTO_BTN,
            bg=COLOR_BTN_CANCELAR, cursor='hand2',
            activebackground=COLOR_BTN_CANCELAR_ACT,
        )
        self.boton_cancelar.grid(column=2, row=9, padx=10, pady=5)

        # Buscador
        tk.Label(
            self, text='Buscar DNI:', font=FUENTE_ETIQUETA,
            bg=COLOR_FONDO, fg=COLOR_TEXTO,
        ).grid(column=3, row=0, padx=10, pady=5)

        tk.Label(
            self, text='Buscar Apellido:', font=FUENTE_ETIQUETA,
            bg=COLOR_FONDO, fg=COLOR_TEXTO,
        ).grid(column=3, row=1, padx=10, pady=5)

        self.var_buscar_dni = tk.StringVar()
        tk.Entry(
            self, textvariable=self.var_buscar_dni, width=20,
            font=FUENTE_ENTRADA, bg=COLOR_SUPERFICIE,
            fg=COLOR_TEXTO, insertbackground=COLOR_TEXTO,
        ).grid(column=4, row=0, padx=10, pady=5, columnspan=2)

        self.var_buscar_apellido = tk.StringVar()
        tk.Entry(
            self, textvariable=self.var_buscar_apellido, width=20,
            font=FUENTE_ENTRADA, bg=COLOR_SUPERFICIE,
            fg=COLOR_TEXTO, insertbackground=COLOR_TEXTO,
        ).grid(column=4, row=1, padx=10, pady=5, columnspan=2)

        tk.Button(
            self, text='Buscar', command=self.buscar_paciente,
            width=20, font=FUENTE_BTN, fg=COLOR_TEXTO_BTN,
            bg=COLOR_BTN_BUSCAR, cursor='hand2',
            activebackground=COLOR_BTN_BUSCAR_ACT,
        ).grid(column=3, row=2, padx=10, pady=5)

        tk.Button(
            self, text='Limpiar', command=self.limpiar_buscador,
            width=20, font=FUENTE_BTN, fg=COLOR_TEXTO_BTN,
            bg=COLOR_BTN_LIMPIAR, cursor='hand2',
            activebackground=COLOR_BTN_LIMPIAR_ACT,
        ).grid(column=4, row=2, padx=10, pady=5)

        self.boton_calendario = tk.Button(
            self, text='Calendario', command=self.abrir_calendario,
            width=12, font=FUENTE_BTN, fg=COLOR_TEXTO_BTN,
            bg=COLOR_BTN_CALENDARIO, cursor='hand2',
            activebackground=COLOR_BTN_CALENDARIO_ACT,
        )
        self.boton_calendario.grid(column=3, row=4, padx=10, pady=5)

    # ── Calendario ───────────────────────────────────────────────────────────

    def abrir_calendario(self):
        """Abre una ventana emergente con un calendario para seleccionar la fecha de nacimiento."""
        self.ventana_calendario = Toplevel()
        self.ventana_calendario.title('FECHA NACIMIENTO')
        self.ventana_calendario.resizable(0, 0)
        self.ventana_calendario.iconbitmap('img/logo.ico')
        self.ventana_calendario.config(bg=COLOR_FONDO)

        self.var_calendario = tk.StringVar()
        fecha_actual = self.var_fecha_nacimiento.get()
        self.var_calendario.set(fecha_actual if fecha_actual else '1990-01-01')

        self.calendario = tc.Calendar(
            self.ventana_calendario, selectmode='day',
            year=1990, month=1, day=1, locale='es_ES',
            bg='#777777', fg='#FFFFFF', headersbackground='#B6DDFE',
            textvariable=self.var_calendario, cursor='hand2',
            date_pattern='y-mm-dd',
        )
        self.calendario.grid(row=1, column=0, pady=22)
        self.var_calendario.trace_add('write', self.actualizar_fecha)

    def actualizar_fecha(self, *args):
        """Copia la fecha seleccionada en el campo de fecha de nacimiento y calcula la edad."""
        fecha_str = self.var_calendario.get()
        self.var_fecha_nacimiento.set(fecha_str)
        if fecha_str:
            try:
                self.calcular_edad(fecha_str)
            except ValueError:
                pass

    def calcular_edad(self, fecha_str):
        """Calcula la edad del paciente a partir de la fecha seleccionada."""
        hoy = date.today()
        fecha_nacimiento = datetime.strptime(fecha_str, '%Y-%m-%d')

        edad = hoy.year - fecha_nacimiento.year
        edad -= (hoy.month, hoy.day) < (fecha_nacimiento.month, fecha_nacimiento.day)
        self.var_edad.set(edad)

    # ── Buscador ─────────────────────────────────────────────────────────────

    def limpiar_buscador(self):
        """Limpia los campos del buscador y recarga la tabla completa de pacientes."""
        self.var_buscar_apellido.set('')
        self.var_buscar_dni.set('')
        self.cargar_tabla_pacientes()

    def buscar_paciente(self):
        """Filtra la tabla de pacientes por DNI o apellido según lo ingresado."""
        dni = self.var_buscar_dni.get().strip()
        apellido = self.var_buscar_apellido.get().strip()

        if not dni and not apellido:
            self.cargar_tabla_pacientes()
            return

        if dni:
            lista_filtrada = buscar_por_dni(dni)
        else:
            lista_filtrada = buscar_por_apellido(apellido)

        self.cargar_tabla_pacientes(lista_filtrada)

    # ── CRUD de paciente ─────────────────────────────────────────────────────

    def guardar_paciente(self):
        """Guarda o actualiza los datos del paciente según corresponda."""
        campos_paciente = [
            self.var_nombre.get(), self.var_apellido_paterno.get(),
            self.var_apellido_materno.get(), self.var_dni.get(),
            self.var_fecha_nacimiento.get(), self.var_edad.get(),
            self.var_antecedentes.get(), self.var_correo.get(),
            self.var_telefono.get()
        ]
        
        if not all(campo.strip() for campo in campos_paciente):
            messagebox.showwarning("Advertencia", "Todas las casillas deben estar llenas para guardar el paciente.")
            return
            
        correo = self.var_correo.get().strip()
        if not re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", correo):
            messagebox.showwarning("Advertencia", "Por favor, ingrese un correo válido.")
            return

        paciente = Persona(
            self.var_nombre.get(), self.var_apellido_paterno.get(),
            self.var_apellido_materno.get(), self.var_dni.get(),
            self.var_fecha_nacimiento.get(), self.var_edad.get(),
            self.var_antecedentes.get(), self.var_correo.get(),
            self.var_telefono.get(),
        )

        if self.id_persona is None:
            registrar_paciente(paciente)
        else:
            actualizar_paciente(paciente, self.id_persona)

        self.deshabilitar_formulario()
        self.cargar_tabla_pacientes()

        if hasattr(self, 'ventana_calendario') and self.ventana_calendario.winfo_exists():
            self.ventana_calendario.destroy()

    def habilitar_formulario(self):
        """Limpia y habilita todos los campos del formulario."""
        for var in (self.var_nombre, self.var_apellido_paterno, self.var_apellido_materno,
                    self.var_dni, self.var_fecha_nacimiento, self.var_edad,
                    self.var_antecedentes, self.var_correo, self.var_telefono):
            var.set('')

        for entrada in self._entradas_formulario:
            entrada.config(state='normal')

        self.boton_guardar.config(state='normal')
        self.boton_cancelar.config(state='normal')
        self.boton_calendario.config(state='normal')

    def deshabilitar_formulario(self):
        """Limpia y deshabilita todos los campos del formulario."""
        self.id_persona = None

        for var in (self.var_nombre, self.var_apellido_paterno, self.var_apellido_materno,
                    self.var_dni, self.var_fecha_nacimiento, self.var_edad,
                    self.var_antecedentes, self.var_correo, self.var_telefono):
            var.set('')

        for entrada in self._entradas_formulario:
            entrada.config(state='disabled')

        self.boton_guardar.config(state='disabled')
        self.boton_cancelar.config(state='disabled')
        self.boton_calendario.config(state='disabled')

    # ── Tabla de pacientes ───────────────────────────────────────────────────

    def cargar_tabla_pacientes(self, lista=None):
        """Crea y pobla la tabla de pacientes. Acepta una lista opcional para filtros."""
        if lista is None:
            lista = obtener_pacientes()

        self.tabla_pacientes = ttk.Treeview(
            self, column=('Nombre', 'APaterno', 'AMaterno', 'Dni',
                          'FNacimiento', 'Edad', 'Antecedentes', 'Correo', 'Telefono'),
        )
        self.tabla_pacientes.grid(column=0, row=10, columnspan=10, sticky='nse')

        barra_vertical = ttk.Scrollbar(
            self, orient='vertical', command=self.tabla_pacientes.yview
        )
        barra_vertical.grid(row=10, column=11, sticky='nse')
        self.tabla_pacientes.configure(yscrollcommand=barra_vertical.set)
        self.tabla_pacientes.tag_configure('fila_par', background=COLOR_FILA_PAR)

        encabezados = [
            ('#0', 'ID'), ('#1', 'Nombre'), ('#2', 'Ap. Paterno'),
            ('#3', 'Ap. Materno'), ('#4', 'DNI'), ('#5', 'F. Nacimiento'),
            ('#6', 'Edad'), ('#7', 'Antecedentes'), ('#8', 'Correo'), ('#9', 'Teléfono'),
        ]
        for columna, titulo in encabezados:
            self.tabla_pacientes.heading(columna, text=titulo)

        anchos = [50, 150, 120, 120, 80, 100, 50, 300, 250, 82]
        for indice, ancho in enumerate(anchos):
            self.tabla_pacientes.column(f'#{indice}', anchor='w', width=ancho)

        for paciente in lista:
            self.tabla_pacientes.insert(
                '', 0, text=paciente[0],
                values=paciente[1:10], tags=('fila_par',),
            )

        # Botones de acción sobre la tabla
        tk.Button(
            self, text='Editar Paciente', command=self.editar_paciente,
            width=20, font=FUENTE_BTN, fg=COLOR_TEXTO_BTN,
            bg=COLOR_BTN_EDITAR, activebackground=COLOR_BTN_EDITAR_ACT, cursor='hand2',
        ).grid(row=11, column=0, padx=10, pady=5)

        tk.Button(
            self, text='Eliminar Paciente', command=self.eliminar_paciente,
            width=20, font=FUENTE_BTN, fg=COLOR_TEXTO_BTN,
            bg=COLOR_BTN_PELIGRO, activebackground=COLOR_BTN_PELIGRO_ACT, cursor='hand2',
        ).grid(row=11, column=1, padx=10, pady=5)

        tk.Button(
            self, text='Historial Paciente', command=self.abrir_historial_medico,
            width=20, font=FUENTE_BTN, fg=COLOR_TEXTO_BTN,
            bg=COLOR_BTN_HISTORIAL, activebackground=COLOR_BTN_HISTORIAL_ACT, cursor='hand2',
        ).grid(row=11, column=2, padx=10, pady=5)

        tk.Button(
            self, text='Salir', command=self.raiz.destroy,
            width=20, font=FUENTE_BTN, fg=COLOR_TEXTO_BTN,
            bg=COLOR_BTN_GUARDAR, activebackground=COLOR_BTN_GUARDAR_ACT, cursor='hand2',
        ).grid(row=11, column=4, padx=10, pady=5)

    def editar_paciente(self):
        """Carga los datos del paciente seleccionado en el formulario para edición."""
        try:
            seleccion = self.tabla_pacientes.selection()
            if not seleccion:
                messagebox.showwarning("Advertencia", "Seleccione un paciente para editar.")
                return
                
            item_seleccionado = self.tabla_pacientes.item(seleccion)
            self.id_persona = item_seleccionado['text']
            valores = item_seleccionado['values']

            self.habilitar_formulario()

            for entrada, valor in zip(self._entradas_formulario, valores[:9]):
                entrada.insert(0, valor)

        except Exception:
            messagebox.showerror('Editar Paciente', 'Error al editar paciente')

    def eliminar_paciente(self):
        """Elimina lógicamente al paciente seleccionado."""
        try:
            seleccion = self.tabla_pacientes.selection()
            if not seleccion:
                messagebox.showwarning("Advertencia", "Seleccione un paciente para eliminar.")
                return
            
            if not messagebox.askyesno("Confirmar", "¿Está seguro de que desea eliminar este paciente?"):
                return
                
            self.id_persona = self.tabla_pacientes.item(seleccion)['text']
            dar_baja_paciente(self.id_persona)
            self.cargar_tabla_pacientes()
            self.id_persona = None
        except Exception:
            messagebox.showinfo('Eliminar Paciente', 'No se pudo eliminar el paciente')

    # ── Historial médico ─────────────────────────────────────────────────────

    def abrir_historial_medico(self):
        """Abre la ventana del historial médico del paciente seleccionado."""
        try:
            if self.id_persona is None:
                self.id_persona = self.tabla_pacientes.item(
                    self.tabla_pacientes.selection()
                )['text']
                self.id_persona_historia = self.id_persona

            if not self.id_persona > 0:
                return

            self.ventana_historial = Toplevel()
            self.ventana_historial.title('HISTORIAL MÉDICO')
            self.ventana_historial.resizable(0, 0)
            self.ventana_historial.iconbitmap('img/logo.ico')
            self.ventana_historial.config(bg=COLOR_FONDO)

            registros = obtener_historias(self.id_persona)

            self.tabla_historial = ttk.Treeview(
                self.ventana_historial,
                column=('Apellidos', 'FechaHistoria', 'Motivo',
                        'ExamenAuxiliar', 'Tratamiento', 'Detalle'),
            )
            self.tabla_historial.grid(row=0, column=0, columnspan=7, sticky='nse')

            barra_historial = ttk.Scrollbar(
                self.ventana_historial, orient='vertical',
                command=self.tabla_historial.yview,
            )
            barra_historial.grid(row=0, column=8, sticky='nse')
            self.tabla_historial.configure(yscrollcommand=barra_historial.set)

            encabezados_historial = [
                ('#0', 'ID'), ('#1', 'Nombre y Apellidos'), ('#2', 'Fecha y Hora'),
                ('#3', 'Motivo'), ('#4', 'Examen Auxiliar'),
                ('#5', 'Tratamiento'), ('#6', 'Detalle'),
            ]
            for columna, titulo in encabezados_historial:
                self.tabla_historial.heading(columna, text=titulo)

            anchos_historial = [50, 150, 100, 120, 250, 200, 450]
            for indice, ancho in enumerate(anchos_historial):
                self.tabla_historial.column(f'#{indice}', anchor='w', width=ancho)

            for registro in registros:
                self.tabla_historial.insert('', 0, text=registro[0], values=registro[1:7])

            tk.Button(
                self.ventana_historial, text='Agregar Historia',
                command=self.abrir_agregar_historia,
                width=20, font=FUENTE_BTN, fg=COLOR_TEXTO_BTN,
                bg=COLOR_BTN_NUEVO, cursor='hand2', activebackground=COLOR_BTN_NUEVO_ACT,
            ).grid(row=2, column=0, padx=10, pady=5)

            tk.Button(
                self.ventana_historial, text='Editar Historia',
                command=self.abrir_editar_historia,
                width=20, font=FUENTE_BTN, fg=COLOR_TEXTO_BTN,
                bg=COLOR_BTN_EDITAR, cursor='hand2', activebackground=COLOR_BTN_EDITAR_ACT,
            ).grid(row=2, column=1, padx=10, pady=5)

            tk.Button(
                self.ventana_historial, text='Eliminar Historia',
                command=self.eliminar_historia_medica,
                width=20, font=FUENTE_BTN, fg=COLOR_TEXTO_BTN,
                bg=COLOR_BTN_PELIGRO, cursor='hand2', activebackground=COLOR_BTN_PELIGRO_ACT,
            ).grid(row=2, column=2, padx=10, pady=5)

            tk.Button(
                self.ventana_historial, text='Salir',
                command=self.cerrar_ventanas_historial,
                width=20, font=FUENTE_BTN, fg=COLOR_TEXTO_BTN,
                bg=COLOR_BTN_GUARDAR, cursor='hand2', activebackground=COLOR_BTN_GUARDAR_ACT,
            ).grid(row=2, column=6, padx=10, pady=5)

            self.id_persona = None

        except Exception:
            messagebox.showerror('Historia Médica', 'Error al mostrar historial')
            self.id_persona = None

    def abrir_agregar_historia(self):
        """Abre la ventana para registrar una nueva historia médica."""
        self.ventana_agregar_historia = Toplevel()
        self.ventana_agregar_historia.title('AGREGAR HISTORIA')
        self.ventana_agregar_historia.resizable(0, 0)
        self.ventana_agregar_historia.iconbitmap('img/logo.ico')
        self.ventana_agregar_historia.config(bg=COLOR_FONDO)

        marco_datos = tk.LabelFrame(
            self.ventana_agregar_historia, bg=COLOR_FONDO, fg=COLOR_TEXTO
        )
        marco_datos.pack(fill='both', expand=True, pady=10, padx=20)

        campos_historia = [
            ('Motivo de la Historia Médica', 'var_motivo_historia', 0),
            ('Examen Auxiliar',              'var_examen_auxiliar', 2),
            ('Tratamiento',                  'var_tratamiento',     4),
            ('Detalle de la Historia Médica','var_detalle_historia', 6),
        ]
        for texto, nombre_var, fila in campos_historia:
            tk.Label(
                marco_datos, text=texto, width=30, font=FUENTE_ETIQUETA,
                bg=COLOR_FONDO, fg=COLOR_TEXTO,
            ).grid(row=fila, column=0, padx=5, pady=3)

            variable = tk.StringVar()
            setattr(self, nombre_var, variable)
            tk.Entry(
                marco_datos, textvariable=variable, width=64,
                font=FUENTE_ENTRADA, bg=COLOR_SUPERFICIE,
                fg=COLOR_TEXTO, insertbackground=COLOR_TEXTO,
            ).grid(row=fila + 1, column=0, padx=5, pady=3, columnspan=2)

        marco_fecha = tk.LabelFrame(
            self.ventana_agregar_historia, bg=COLOR_FONDO, fg=COLOR_TEXTO
        )
        marco_fecha.pack(fill='both', expand=True, padx=20, pady=10)

        tk.Label(
            marco_fecha, text='Fecha y Hora', width=20, font=FUENTE_ETIQUETA,
            bg=COLOR_FONDO, fg=COLOR_TEXTO,
        ).grid(row=1, column=0, padx=5, pady=3)

        self.var_fecha_historia = tk.StringVar()
        self.var_fecha_historia.set(datetime.today().strftime('%Y-%m-%d %H:%M'))
        tk.Entry(
            marco_fecha, textvariable=self.var_fecha_historia, width=20,
            font=FUENTE_ENTRADA, bg=COLOR_SUPERFICIE,
            fg=COLOR_TEXTO, insertbackground=COLOR_TEXTO,
        ).grid(row=1, column=1, padx=5, pady=3)

        tk.Button(
            marco_fecha, text='Agregar Historia', command=self.guardar_historia_medica,
            width=20, font=FUENTE_BTN, fg=COLOR_TEXTO_BTN,
            bg=COLOR_BTN_NUEVO, cursor='hand2', activebackground=COLOR_BTN_NUEVO_ACT,
        ).grid(row=2, column=0, padx=10, pady=5)

        tk.Button(
            marco_fecha, text='Salir',
            command=self.ventana_agregar_historia.destroy,
            width=20, font=FUENTE_BTN, fg=COLOR_TEXTO_BTN,
            bg=COLOR_BTN_GUARDAR, cursor='hand2', activebackground=COLOR_BTN_GUARDAR_ACT,
        ).grid(row=2, column=3, padx=10, pady=5)

        self.id_persona = None

    def guardar_historia_medica(self):
        """Persiste la nueva historia médica en la base de datos."""
        campos_historia = [
            self.var_fecha_historia.get(),
            self.var_motivo_historia.get(),
            self.var_examen_auxiliar.get(),
            self.var_tratamiento.get(),
            self.var_detalle_historia.get()
        ]
        
        if not all(campo.strip() for campo in campos_historia):
            messagebox.showwarning("Advertencia", "Todas las casillas deben estar llenas para guardar la historia médica.")
            return

        try:
            if self.id_historia_medica is None:
                registrar_historia(
                    self.id_persona_historia,
                    self.var_fecha_historia.get(),
                    self.var_motivo_historia.get(),
                    self.var_examen_auxiliar.get(),
                    self.var_tratamiento.get(),
                    self.var_detalle_historia.get(),
                )
            self.ventana_agregar_historia.destroy()
            self.ventana_historial.destroy()
            self.id_persona = None
        except Exception:
            messagebox.showerror('Agregar Historia', 'Error al agregar historia médica')

    def eliminar_historia_medica(self):
        """Elimina la historia médica seleccionada de la base de datos."""
        try:
            seleccion = self.tabla_historial.selection()
            if not seleccion:
                messagebox.showwarning("Advertencia", "Seleccione una historia médica para eliminar.")
                return
                
            if not messagebox.askyesno("Confirmar", "¿Está seguro de que desea eliminar esta historia médica?"):
                return
                
            self.id_historia_medica = self.tabla_historial.item(seleccion)['text']
            borrar_historia(self.id_historia_medica)
            self.id_historia_medica = None
            self.ventana_historial.destroy()
        except Exception:
            messagebox.showerror('Eliminar Historia', 'Error al eliminar historia')

    def abrir_editar_historia(self):
        """Abre la ventana para editar la historia médica seleccionada."""
        try:
            seleccion = self.tabla_historial.item(self.tabla_historial.selection())
            self.id_historia_medica = seleccion['text']
            valores = seleccion['values']

            fecha_actual        = valores[1]
            motivo_actual       = valores[2]
            examen_actual       = valores[3]
            tratamiento_actual  = valores[4]
            detalle_actual      = valores[5]

            self.ventana_editar_historia = Toplevel()
            self.ventana_editar_historia.title('EDITAR HISTORIA MÉDICA')
            self.ventana_editar_historia.resizable(0, 0)
            self.ventana_editar_historia.iconbitmap('img/logo.ico')
            self.ventana_editar_historia.config(bg=COLOR_FONDO)

            marco_editar = tk.LabelFrame(
                self.ventana_editar_historia, bg=COLOR_FONDO, fg=COLOR_TEXTO
            )
            marco_editar.pack(fill='both', expand=True, padx=20, pady=10)

            campos_editar = [
                ('Motivo de la historia',  'var_motivo_editar',          motivo_actual,      0),
                ('Examen Auxiliar',        'var_examen_auxiliar_editar',  examen_actual,      2),
                ('Tratamiento',            'var_tratamiento_editar',      tratamiento_actual, 4),
                ('Detalle de la historia', 'var_detalle_editar',          detalle_actual,     6),
            ]
            for texto, nombre_var, valor_actual, fila in campos_editar:
                tk.Label(
                    marco_editar, text=texto, width=30, font=FUENTE_ETIQUETA,
                    bg=COLOR_FONDO, fg=COLOR_TEXTO,
                ).grid(row=fila, column=0, padx=5, pady=3)

                variable = tk.StringVar()
                setattr(self, nombre_var, variable)
                entrada = tk.Entry(
                    marco_editar, textvariable=variable, width=65,
                    font=FUENTE_ENTRADA, bg=COLOR_SUPERFICIE,
                    fg=COLOR_TEXTO, insertbackground=COLOR_TEXTO,
                )
                entrada.grid(row=fila + 1, column=0, pady=3, padx=5, columnspan=2)
                entrada.insert(0, valor_actual)

            marco_fecha_editar = tk.LabelFrame(
                self.ventana_editar_historia, bg=COLOR_FONDO, fg=COLOR_TEXTO
            )
            marco_fecha_editar.pack(fill='both', expand=True, padx=20, pady=10)

            tk.Label(
                marco_fecha_editar, text='Fecha y Hora', width=30,
                font=FUENTE_ETIQUETA, bg=COLOR_FONDO, fg=COLOR_TEXTO,
            ).grid(row=1, column=0, padx=5, pady=3)

            self.var_fecha_historia_editar = tk.StringVar()
            entrada_fecha = tk.Entry(
                marco_fecha_editar, textvariable=self.var_fecha_historia_editar,
                width=20, font=FUENTE_ENTRADA, bg=COLOR_SUPERFICIE,
                fg=COLOR_TEXTO, insertbackground=COLOR_TEXTO,
            )
            entrada_fecha.grid(row=1, column=1, pady=3, padx=5)
            entrada_fecha.insert(0, fecha_actual)

            tk.Button(
                marco_fecha_editar, text='Editar Historia',
                command=self.confirmar_editar_historia,
                width=20, font=FUENTE_BTN, fg=COLOR_TEXTO_BTN,
                bg=COLOR_BTN_EDITAR, cursor='hand2', activebackground=COLOR_BTN_EDITAR_ACT,
            ).grid(row=2, column=0, padx=10, pady=5)

            tk.Button(
                marco_fecha_editar, text='Salir',
                command=self.ventana_editar_historia.destroy,
                width=20, font=FUENTE_BTN, fg=COLOR_TEXTO_BTN,
                bg=COLOR_BTN_GUARDAR, cursor='hand2', activebackground=COLOR_BTN_GUARDAR_ACT,
            ).grid(row=2, column=1, padx=10, pady=5)

            if self.id_historia_medica_editar is None:
                self.id_historia_medica_editar = self.id_historia_medica

            self.id_historia_medica = None

        except Exception:
            messagebox.showerror('Editar Historia', 'Error al editar historia')

    def confirmar_editar_historia(self):
        """Persiste los cambios de edición de una historia médica en la base de datos."""
        campos_editar = [
            self.var_fecha_historia_editar.get(),
            self.var_motivo_editar.get(),
            self.var_examen_auxiliar_editar.get(),
            self.var_tratamiento_editar.get(),
            self.var_detalle_editar.get()
        ]
        
        if not all(campo.strip() for campo in campos_editar):
            messagebox.showwarning("Advertencia", "Todas las casillas deben estar llenas para editar la historia médica.")
            return

        try:
            actualizar_historia(
                self.var_fecha_historia_editar.get(),
                self.var_motivo_editar.get(),
                self.var_examen_auxiliar_editar.get(),
                self.var_tratamiento_editar.get(),
                self.var_detalle_editar.get(),
                self.id_historia_medica_editar,
            )
            self.id_historia_medica_editar = None
            self.id_historia_medica = None
            self.ventana_editar_historia.destroy()
            self.ventana_historial.destroy()
        except Exception:
            messagebox.showerror('Editar Historia', 'Error al editar historia')
            self.ventana_editar_historia.destroy()

    def cerrar_ventanas_historial(self):
        """Cierra todas las ventanas relacionadas con el historial médico."""
        for nombre in ('ventana_historial', 'ventana_agregar_historia', 'ventana_editar_historia'):
            ventana = getattr(self, nombre, None)
            if ventana and ventana.winfo_exists():
                ventana.destroy()
        self.id_persona = None
