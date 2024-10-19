import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget, QTableWidget, QTableWidgetItem, QMessageBox, QProgressBar, QDialog
from PyQt5.QtGui import QFont, QIntValidator
from Planificación_Procesos.modules.Proceso import Proceso
from Planificación_Procesos.modules.gestor_procesos import GestorProcesos

class ResultadosDialog(QDialog):
    def __init__(self, tme, tmr, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Resultados: TME y TMR")
        self.setGeometry(200, 200, 400, 200)

        # Aplicar estilo a toda la ventana emergente
        self.setStyleSheet(self.estilo_ventana_emergente())

        layout = QVBoxLayout()

        # Etiquetas para mostrar TME y TMR
        self.label_tme = QLabel(f"Tiempo Medio de Espera (TME): {tme:.2f} unidades de tiempo", self)
        self.label_tme.setFont(QFont('Helvetica', 12))
        layout.addWidget(self.label_tme)

        self.label_tmr = QLabel(f"Tiempo Medio de Retorno (TMR): {tmr:.2f} unidades de tiempo", self)
        self.label_tmr.setFont(QFont('Helvetica', 12))
        layout.addWidget(self.label_tmr)

        # Botón para cerrar la ventana
        self.boton_cerrar = QPushButton("Cerrar", self)
        self.boton_cerrar.setStyleSheet(self.estilo_boton_fusion())
        self.boton_cerrar.clicked.connect(self.close)
        layout.addWidget(self.boton_cerrar)

        self.setLayout(layout)

    def estilo_ventana_emergente(self):
        return """
            QDialog {
                background-color: #F0F0F0;
                border: 1px solid #A9A9A9;
                border-radius: 10px;
                padding: 10px;
            }
            QLabel {
                color: #333333;
                font-size: 14px;
            }
        """

    def estilo_boton_fusion(self):
        return """
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border-radius: 5px;
                padding: 5px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #3e8e41;
            }
        """


class Aplicacion(QMainWindow):
    def __init__(self):
        super().__init__()
        self.gestor_procesos = GestorProcesos()  # Instancia del gestor de procesos
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Priority Scheduling Algorithm")
        self.setGeometry(100, 100, 700, 600)

        layout = QVBoxLayout()

        # Campos de entrada
        self.entrada_nombre = self.crear_campo("Nombre del Proceso:", layout)
        self.entrada_tiempo_ejecucion = self.crear_campo("Ráfaga de CPU:", layout, validar=self.validar_numeros)
        self.entrada_tiempo_llegada = self.crear_campo("Tiempo de Llegada:", layout, validar=self.validar_numeros)
        self.entrada_prioridad = self.crear_campo("Prioridad:", layout, validar=self.validar_numeros)

        # Mover con Enter entre campos
        self.entrada_nombre.returnPressed.connect(self.entrada_tiempo_ejecucion.setFocus)
        self.entrada_tiempo_ejecucion.returnPressed.connect(self.entrada_tiempo_llegada.setFocus)
        self.entrada_tiempo_llegada.returnPressed.connect(self.entrada_prioridad.setFocus)
        self.entrada_prioridad.returnPressed.connect(self.agregar_proceso)

        # Botones
        self.boton_agregar = QPushButton("Agregar Proceso", self)
        self.boton_agregar.setFont(QFont('Helvetica', 12))
        self.boton_agregar.setStyleSheet(self.estilo_boton_fusion())
        self.boton_agregar.clicked.connect(self.agregar_proceso)
        layout.addWidget(self.boton_agregar)

        self.boton_ejecutar = QPushButton("Ejecutar Planificación", self)
        self.boton_ejecutar.setFont(QFont('Helvetica', 12))
        self.boton_ejecutar.setStyleSheet(self.estilo_boton_fusion())
        self.boton_ejecutar.clicked.connect(self.ejecutar_planificacion)
        layout.addWidget(self.boton_ejecutar)

        self.boton_nueva = QPushButton("Nueva Planificación", self)
        self.boton_nueva.setFont(QFont('Helvetica', 12))
        self.boton_nueva.setStyleSheet(self.estilo_boton_fusion())
        self.boton_nueva.clicked.connect(self.nueva_planificacion)
        layout.addWidget(self.boton_nueva)

        # Crear tabla
        self.tabla = QTableWidget(self)
        self.tabla.setColumnCount(6)
        self.tabla.setHorizontalHeaderLabels(['Proceso', 'Ráfaga CPU', 'Prioridad', 'Tiempo Espera', 'Inicio', 'Fin'])
        self.tabla.setStyleSheet(self.estilo_tabla_fusion())
        layout.addWidget(self.tabla)

        # Crear barra de progreso
        self.barra_progreso = QProgressBar(self)
        self.barra_progreso.setStyleSheet(self.estilo_progreso_fusion())
        layout.addWidget(self.barra_progreso)

        # Crear un widget central para poner el layout
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def crear_campo(self, texto, layout, validar=None):
        etiqueta = QLabel(texto, self)
        etiqueta.setFont(QFont('Helvetica', 12))
        layout.addWidget(etiqueta)

        entrada = QLineEdit(self)
        entrada.setFont(QFont('Helvetica', 12))
        entrada.setStyleSheet(self.estilo_input_fusion())
        if validar:
            entrada.setValidator(QIntValidator(0, 1000, self))  # Solo permite números no negativos
        layout.addWidget(entrada)

        return entrada

    def validar_numeros(self, texto):
        if not texto.isdigit():
            self.sender().setText("")

    def agregar_proceso(self):
        nombre = self.entrada_nombre.text().strip()
        if not self.validar_campos(nombre):
            return

        # Comprobar si el proceso ya existe
        if self.proceso_ya_existe(nombre):
            QMessageBox.critical(self, "Error", f"El proceso '{nombre}' ya existe.")
            return

        try:
            tiempo_ejecucion = int(self.entrada_tiempo_ejecucion.text())
            tiempo_llegada = int(self.entrada_tiempo_llegada.text())
            prioridad = int(self.entrada_prioridad.text())

            proceso = Proceso(nombre, tiempo_llegada, tiempo_ejecucion, prioridad)
            self.gestor_procesos.agregar_proceso(proceso)
            self.actualizar_tabla()
            self.limpiar_campos()

            # Mostrar ventana emergente
            QMessageBox.information(self, "Información", f"Proceso '{nombre}' agregado correctamente.")

        except ValueError as e:
            QMessageBox.critical(self, "Error", str(e))

    def proceso_ya_existe(self, nombre):
        # Comprueba si un proceso con el mismo nombre ya ha sido agregado
        for proceso in self.gestor_procesos.procesos:
            if proceso.nombre == nombre:
                return True
        return False

    def validar_campos(self, nombre):
        if not nombre:
            QMessageBox.critical(self, "Error", "Ingrese el nombre del Proceso.")
            self.entrada_nombre.setFocus()
            return False
        if not self.entrada_tiempo_ejecucion.text().strip():
            QMessageBox.critical(self, "Error", "Ingrese la Ráfaga de CPU.")
            self.entrada_tiempo_ejecucion.setFocus()
            return False
        if not self.entrada_tiempo_llegada.text().strip():
            QMessageBox.critical(self, "Error", "Ingrese el Tiempo de Llegada.")
            self.entrada_tiempo_llegada.setFocus()
            return False
        if not self.entrada_prioridad.text().strip():
            QMessageBox.critical(self, "Error", "Ingrese la Prioridad.")
            self.entrada_prioridad.setFocus()
            return False
        return True

    def limpiar_campos(self):
        self.entrada_nombre.clear()
        self.entrada_tiempo_ejecucion.clear()
        self.entrada_tiempo_llegada.clear()
        self.entrada_prioridad.clear()
        self.entrada_nombre.setFocus()

    def actualizar_tabla(self):
        self.tabla.setRowCount(0)  # Limpiar la tabla
        for proceso in self.gestor_procesos.planificar_por_prioridad():
            row_position = self.tabla.rowCount()
            self.tabla.insertRow(row_position)
            self.tabla.setItem(row_position, 0, QTableWidgetItem(proceso[0]))
            self.tabla.setItem(row_position, 1, QTableWidgetItem(str(proceso[1])))
            self.tabla.setItem(row_position, 2, QTableWidgetItem(str(proceso[3])))
            self.tabla.setItem(row_position, 3, QTableWidgetItem(str(proceso[4])))
            self.tabla.setItem(row_position, 4, QTableWidgetItem(str(proceso[6])))
            self.tabla.setItem(row_position, 5, QTableWidgetItem(str(proceso[7])))

    def ejecutar_planificacion(self):
        self.barra_progreso.setValue(0)
        self.barra_progreso.setMaximum(100)
        self.barra_progreso.setValue(100)

        # Cálculos de TME y TMR
        tme, tmr, total_espera, total_retorno = self.gestor_procesos.calcular_promedios()

        # Mostrar resultados en la ventana separada
        self.mostrar_resultados(tme, tmr)

    def mostrar_resultados(self, tme, tmr):
        # Crear una ventana de diálogo para mostrar los resultados de TME y TMR
        dialogo_resultados = ResultadosDialog(tme, tmr, self)
        dialogo_resultados.exec_()

    def nueva_planificacion(self):
        self.tabla.setRowCount(0)
        self.limpiar_campos()
        self.gestor_procesos.limpiar_procesos()

    # Métodos para los estilos fusionados
    def estilo_boton_fusion(self):
        return """
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border-radius: 5px;
                padding: 5px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #3e8e41;
            }
        """

    def estilo_input_fusion(self):
        return """
            QLineEdit {
                background-color: white;
                border: 1px solid #CCCCCC;
                padding: 5px;
                font-size: 14px;
            }
        """

    def estilo_tabla_fusion(self):
        return """
            QTableWidget {
                background-color: white;
                border: 1px solid #CCCCCC;
                font-size: 12px;
            }
            QHeaderView::section {
                background-color: #EAEAEA;
                padding: 4px;
                font-size: 14px;
                color: #555555;
                border: 1px solid #CCCCCC;
            }
        """

    def estilo_progreso_fusion(self):
        return """
            QProgressBar {
                border: 1px solid #CCCCCC;
                background: #F3F3F3;
                height: 10px;
            }
            QProgressBar::chunk {
                background-color: #4CAF50;
            }
        """

if __name__ == '__main__':
    app = QApplication(sys.argv)

    # Aplicar el estilo "Fusion"
    app.setStyle('Fusion')

    ventana = Aplicacion()
    ventana.show()

    sys.exit(app.exec_())
