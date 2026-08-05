import sqlite3


class ConexionBaseDatos:
    """Gestiona la conexión con la base de datos"""

    _RUTA_BD = 'database/dbhistorial.db'

    def __init__(self):
        self.conexion = sqlite3.connect(self._RUTA_BD)
        self.cursor = self.conexion.cursor()

    def cerrar_conexion(self):
        self.conexion.commit()
        self.conexion.close()
