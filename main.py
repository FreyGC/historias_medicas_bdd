import os
import sys

_directorio_base = os.path.dirname(os.path.abspath(__file__))
os.chdir(_directorio_base)
if _directorio_base not in sys.path:
    sys.path.append(_directorio_base)

import tkinter as tk
from gui.interfaz import MarcoSistema


def main():
    raiz = tk.Tk()
    raiz.title('Historias Médicas Odontológicas')
    raiz.resizable(0, 0)
    raiz.iconbitmap('img/logo.ico')
    marco = MarcoSistema(raiz)
    marco.mainloop()


if __name__ == '__main__':
    main()
