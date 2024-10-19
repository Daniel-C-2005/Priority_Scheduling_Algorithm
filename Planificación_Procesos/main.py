import sys
import os
from PyQt5.QtWidgets import QApplication
from aplicacion import Aplicacion

# Asegúrate de que el path al módulo Planificación_Procesos esté disponible
sys.path.append(os.path.abspath("/Planificación_Procesos"))

if __name__ == "__main__":
    app = QApplication(sys.argv)  # Inicializamos la aplicación PyQt5
    ventana = Aplicacion()  # Creamos una instancia de la clase Aplicacion (heredada de QMainWindow)
    ventana.show()  # Mostramos la ventana principal
    sys.exit(app.exec_())  # Iniciamos el loop de la aplicación
