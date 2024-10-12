# main.py
import tkinter as tk
import sys
import os

sys.path.append(os.path.abspath("/Planificación_Procesos"))

# Import the Aplicacion class
from aplicacion import Aplicacion

if __name__ == "__main__":
    root = tk.Tk()
    app = Aplicacion(root)  # Creamos una instancia de Aplicacion
    root.mainloop()