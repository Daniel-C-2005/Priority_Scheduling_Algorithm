import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget, \
    QTableWidget, QTableWidgetItem, QMessageBox, QProgressBar, QDialog, QHeaderView
from PyQt5.QtGui import QFont, QIntValidator
from Planificación_Procesos.modules.Proceso import Proceso
from Planificación_Procesos.modules.gestor_procesos import GestorProcesos

class ResultadosDialog(QDialog):
    def __init__(self, tme, tmr, detalles_tme_tmr, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Resultados: TME y TMR")
        self.setGeometry(200, 200, 600, 400)

        layout = QVBoxLayout()

        # Mostrar los resultados de TME y TMR
        self.label_tme = QLabel(f"TME (Tiempo Medio de Espera): {tme:.2f} unidades de tiempo", self)
        self.label_tme.setFont(QFont('Helvetica', 12))
        layout.addWidget(self.label_tme)

        self.label_tmr = QLabel(f"TMR (Tiempo Medio de Retorno): {tmr:.2f} unidades de tiempo", self)
        self.label_tmr.setFont(QFont('Helvetica', 12))
        layout.addWidget(self.label_tmr)

        # Mostrar detalle de los cálculos para cada proceso
        self.label_detalle = QLabel("Desglose de cálculos:", self)
        self.label_detalle.setFont(QFont('Helvetica', 12))
        layout.addWidget(self.label_detalle)

        for detalle in detalles_tme_tmr:
            nombre_proceso = detalle['nombre']
            espera = detalle['tiempo_espera']
            retorno = detalle['tiempo_retorno']
            layout.addWidget(QLabel(f"Proceso {nombre_proceso}: Tiempo de Espera = {espera} ut, Tiempo de Retorno = {retorno} ut", self))

        # Botón para cerrar la ventana
        self.boton_cerrar = QPushButton("Cerrar", self)
        self.boton_cerrar.setStyleSheet("""
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
        """)
        self.boton_cerrar.clicked.connect(self.close)
        layout.addWidget(self.boton_cerrar)

        self.setLayout(layout)


class Aplicacion(QMainWindow):
    def __init__(self):
        super().__init__()
        self.gestor_procesos = GestorProcesos()  # Instancia del gestor de procesos
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Priority Scheduling Algorithm")
        self.setGeometry(100, 100, 700, 600)

        # Aplicar fondo con degradado de verde fuerte a azul claro
        self.setStyleSheet("""
              QMainWindow {
                  background: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #4CAF50, stop:1 #2196F3);
              }
          """)

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

        # Estilo negrita para el encabezado de la tabla
        header = self.tabla.horizontalHeader()
        header.setStyleSheet("QHeaderView::section { font-weight: bold; }")

        # Ajustar el tamaño de las columnas al contenido
        self.tabla.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

        # Ajustar todas columnas para que se expandan y llenen el espacio restante
        self.tabla.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

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
            self.tabla.setItem(row_position, 3, QTableWidgetItem(f"{proceso[4]} ut"))  # Agrega "ut" al final
            self.tabla.setItem(row_position, 4, QTableWidgetItem(f"{proceso[6]} ut"))  # Agrega "ut"
            self.tabla.setItem(row_position, 5, QTableWidgetItem(f"{proceso[7]} ut"))  # Agrega "ut"

    def ejecutar_planificacion(self):
        self.barra_progreso.setValue(0)
        self.barra_progreso.setMaximum(100)
        self.barra_progreso.setValue(100)

        # Cálculos de TME y TMR
        try:
            # Verifica que el gestor de procesos tenga procesos antes de calcular
            if len(self.gestor_procesos.procesos) == 0:
                QMessageBox.warning(self, "Advertencia", "No hay procesos para planificar.")
                return

            # Llamada al cálculo de promedios
            tme, tmr, detalles_tme_tmr = self.gestor_procesos.calcular_promedios()

            # Debug para asegurarte que los valores se calculan correctamente
            print(f"TME: {tme}, TMR: {tmr}, Detalles: {detalles_tme_tmr}")

            # Mostrar ventana emergente con los detalles del cálculo
            dialogo_resultados = ResultadosDialog(tme, tmr, detalles_tme_tmr, self)
            dialogo_resultados.exec_()  # Asegúrate de usar exec_ para mostrar el diálogo de forma modal

        except Exception as e:
            # Mensaje de error en caso de fallo en la planificación
            QMessageBox.critical(self, "Error", f"Se produjo un error durante la planificación: {str(e)}")

    def nueva_planificacion(self):
        self.tabla.setRowCount(0)
        self.limpiar_campos()
        self.gestor_procesos.limpiar_procesos()

    # Métodos para los estilos fusionados
    def estilo_boton_fusion(self):
        return """
            QPushButton {
                background-color: transparent;
                color: white;
                border-radius: 15px;  /* Borde redondeado */
                padding: 10px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: SKYBLUE;
            }
            QPushButton:pressed {
                background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 blue, stop:1  skyblue);
            }
        """

    def estilo_input_fusion(self):
        return """
            QLineEdit {
                background-color: white;
                border: 1px solid #CCCCCC;
                border-radius: 15px;  /* Borde redondeado */
                padding: 5px;
                font-size: 14px;
            }
        """

    def estilo_tabla_fusion(self):
        return """
            QTableWidget {
                background-color: white;
                border: 2px solid #CCCCCC;
                font-size: 12px;
            }
            QHeaderView::section {
                background-color: #EAEAEA;
                padding: 4px;
                font-size: 14px;
                color: #555555;
                border: 2px solid #CCCCCC;
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

