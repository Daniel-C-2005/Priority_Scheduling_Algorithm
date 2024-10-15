import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
import threading
from Planificación_Procesos.modules.Proceso import Proceso
from Planificación_Procesos.modules.gestor_procesos import GestorProcesos


class Aplicacion:
    def __init__(self, ventana):
        self.ventana = ventana
        self.gestor_procesos = GestorProcesos()  # Instancia del gestor de procesos
        self.crear_interfaz()
        self.ventana_emergente = None  # Variable para almacenar la ventana emergente abierta

    def crear_interfaz(self):
        self.ventana.title("Priority Scheduling Algorithm")
        self.ventana.geometry("700x600")
        #Fondo celeste
        self.ventana.configure(bg="dodger blue")
        self.crear_entradas_y_etiquetas()
        self.crear_botones()
        self.crear_tabla()
        self.crear_barra_progreso()
        self.crear_canvas_secuencia()  # Crear el canvas para la secuencia

        self.entrada_nombre.focus()

    def crear_entradas_y_etiquetas(self):
        self.entrada_nombre = self.crear_campo("Nombre del Proceso:", validar=None)
        self.entrada_tiempo_ejecucion = self.crear_campo("Ráfaga de CPU:", validar=self.validar_numeros)
        self.entrada_tiempo_llegada = self.crear_campo("Tiempo de Llegada:", validar=self.validar_numeros)
        self.entrada_prioridad = self.crear_campo("Prioridad:", validar=self.validar_numeros)

        # Atajos de teclado para mover entre los campos con la tecla Enter
        self.entrada_nombre.bind("<Return>", lambda event: self.entrada_tiempo_ejecucion.focus_set())
        self.entrada_tiempo_ejecucion.bind("<Return>", lambda event: self.entrada_tiempo_llegada.focus_set())
        self.entrada_tiempo_llegada.bind("<Return>", lambda event: self.entrada_prioridad.focus_set())
        self.entrada_prioridad.bind("<Return>", lambda event: self.agregar_proceso())

    def crear_campo(self, texto, validar):
        etiqueta = tk.Label(self.ventana, text=texto, bg="dodger blue", font=('Comic Sans MS', 12, 'bold'))
        etiqueta.pack(pady=5)

        entrada = tk.Entry(self.ventana, bg="#ffffff", font=('Helvetica', 12), bd=1)
        entrada.pack(pady=5)
        if validar:
            entrada.config(validate="key", validatecommand=(self.ventana.register(validar), '%P'))
        return entrada

    def validar_numeros(self, nuevo_texto):
        return nuevo_texto.isdigit() or nuevo_texto == ""

    def crear_botones(self):
        tk.Button(self.ventana, text="Agregar Proceso", command=self.agregar_proceso, bg="#4CAF50", fg="white",
                  font=('Verdana', 12,"bold")).pack(pady=5)
        tk.Button(self.ventana, text="Ejecutar Planificación", command=self.ejecutar_planificacion, bg="#2196F3",
                  fg="white", font=('Verdana', 12, "bold")).pack(pady=5)
        tk.Button(self.ventana, text="Nueva Planificación", command=self.nueva_planificacion, bg="#FF5722",
                  fg="white", font=('Verdana', 12,"bold")).pack(pady=5)

    def crear_tabla(self):
        self.tabla = ttk.Treeview(self.ventana,
                                  columns=('Proceso', 'Ráfaga CPU', 'Prioridad', 'Tiempo Espera', 'Inicio', 'Fin'),
                                  show='headings')
        self.tabla.heading('Proceso', text='Proceso')
        self.tabla.heading('Ráfaga CPU', text='Ráfaga CPU')
        self.tabla.heading('Prioridad', text='Prioridad')
        self.tabla.heading('Tiempo Espera', text='Tiempo Espera')
        self.tabla.heading('Inicio', text='Inicio')
        self.tabla.heading('Fin', text='Fin')

        # Configurar tamaño de las columnas
        self.tabla.column('Proceso', anchor='center', width=70)  # Tamaño para la columna 'Proceso'
        self.tabla.column('Ráfaga CPU', anchor='center', width=70)  # Tamaño para la columna 'Ráfaga CPU'
        self.tabla.column('Prioridad', anchor='center', width=70)  # Tamaño para la columna 'Prioridad'
        self.tabla.column('Tiempo Espera', anchor='center', width=70)  # Tamaño para la columna 'Tiempo Espera'
        self.tabla.column('Inicio', anchor='center', width=70)  # Tamaño para la columna 'Inicio'
        self.tabla.column('Fin', anchor='center', width=70)  # Tamaño para la columna 'Fin'

        self.tabla.pack(pady=10, fill=tk.BOTH, expand=True)

    def crear_barra_progreso(self):
        self.barra_progreso = ttk.Progressbar(self.ventana, mode='indeterminate')
        self.barra_progreso.pack(pady=10, fill=tk.X)

    def crear_canvas_secuencia(self):
        self.canvas = tk.Canvas(self.ventana, height=150, bg="white")  # Altura aumentada para mayor claridad
        self.canvas.pack(pady=10, fill=tk.BOTH, expand=True)


    def agregar_proceso(self):
        nombre = self.entrada_nombre.get().strip()
        if not self.validar_campos(nombre):
            return

        try:
            tiempo_ejecucion = int(self.entrada_tiempo_ejecucion.get())
            tiempo_llegada = int(self.entrada_tiempo_llegada.get())
            prioridad = int(self.entrada_prioridad.get())

            proceso = Proceso(nombre, tiempo_llegada, tiempo_ejecucion, prioridad)
            self.gestor_procesos.agregar_proceso(proceso)
            self.actualizar_tabla()
            self.limpiar_campos()

            # Mostrar ventana emergente y cerrar con Enter
            self.ventana_emergente = messagebox.showinfo("Información", f"Proceso '{nombre}' agregado correctamente.")
            self.ventana.bind("<Return>", self.cerrar_ventana_emergente)

        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def cerrar_ventana_emergente(self, event):
        if self.ventana_emergente is not None:
            self.ventana_emergente = None  # Limpiamos la referencia a la ventana emergente
            self.ventana.unbind("<Return>")  # Desactivamos el binding para evitar conflictos
            messagebox.destroy()  # Cerrar cualquier ventana emergente de Tkinter

    def validar_campos(self, nombre):
        if not nombre:
            messagebox.showerror("Error", "Ingrese el nombre del Proceso.")
            self.entrada_nombre.focus()
            #agregar metodo para limpiar campos

            return False
        if not self.entrada_tiempo_ejecucion.get().strip():
            messagebox.showerror("Error", "Ingrese la Ráfaga de CPU.")
            self.entrada_tiempo_ejecucion.focus()
            return False
        if not self.entrada_tiempo_llegada.get().strip():
            messagebox.showerror("Error", "Ingrese el Tiempo de Llegada.")
            self.entrada_tiempo_llegada.focus()

            return False
        if not self.entrada_prioridad.get().strip():
            messagebox.showerror("Error", "Ingrese la Prioridad.")
            self.entrada_prioridad.focus()
            return False
        return True

    def limpiar_campos(self):
        self.entrada_nombre.delete(0, tk.END)
        self.entrada_tiempo_ejecucion.delete(0, tk.END)
        self.entrada_tiempo_llegada.delete(0, tk.END)
        self.entrada_prioridad.delete(0, tk.END)
        self.entrada_nombre.focus()

    def actualizar_tabla(self):
        for item in self.tabla.get_children():
            self.tabla.delete(item)
        for proceso in self.gestor_procesos.planificar_por_prioridad():
            tiempo_espera_ut = f"{proceso[4]}ut"  # Tiempo de espera con el formato de operación
            inicio_ut = f"{proceso[6]} ut"  # Tiempo de inicio
            fin_ut = f"{proceso[7]} ut"  # Tiempo de finalización
            self.tabla.insert("", tk.END,
                              values=(proceso[0], proceso[1], proceso[3], tiempo_espera_ut, inicio_ut, fin_ut))

    def ejecutar_planificacion(self):
        self.barra_progreso.start(10)
        threading.Thread(target=self.planificar).start()

    def planificar(self):
        try:
            resultado = self.gestor_procesos.planificar_por_prioridad()
            self.mostrar_resultados(resultado)
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            self.barra_progreso.stop()

    def mostrar_resultados(self, resultado):
        self.limpiar_tabla()
        self.canvas.delete("all")  # Limpiar el Canvas antes de dibujar la nueva secuencia
        secuencia_ejecucion = "Secuencia de Ejecución: "
        x_actual = 50  # Coordenada inicial en el canvas, ajustada para más claridad
        y = 50  # Altura fija para las barras
        height = 30  # Altura de cada barra
        escala = 40  # Escala para representar las unidades de tiempo

        for proceso in resultado:
            inicio = x_actual
            duracion = proceso[1] * escala  # Ajustar la duración a la escala
            fin = inicio + duracion

            # Dibujar el rectángulo (barra de proceso)
            self.canvas.create_rectangle(inicio, y, fin, y + height, fill="lightblue", outline="black")
            self.canvas.create_text((inicio + fin) // 2, y + height / 2, text=proceso[0], font=('Helvetica', 10))

            # Dibujar los tiempos
            self.canvas.create_text(inicio, y + height + 10, text=str(proceso[6]),
                                    font=('Helvetica', 10))  # Tiempo de inicio
            self.canvas.create_text(fin, y + height + 10, text=str(proceso[7]),
                                    font=('Helvetica', 10))  # Tiempo de finalización

            # Actualizar la secuencia de ejecución mostrando el nombre del proceso, tiempo de inicio y tiempo de retorno
            secuencia_ejecucion += f"{proceso[0]} ({proceso[6]}-{proceso[7]}) -> "
            x_actual = fin + 10  # Ajustar la posición para el siguiente proceso

        # Calcular promedios y obtener sumas parciales
        tme, tmr, total_espera, total_retorno = self.gestor_procesos.calcular_promedios()

        # Obtener la cantidad de procesos
        n = len(self.gestor_procesos.procesos)

        # Crear la operación lógica para TME y TMR
        tme_formula = "TME=(" + "+".join(
            str(p.tiempo_espera) for p in self.gestor_procesos.procesos) + f")/{n}={tme:.2f} ut"

        # Usar los tiempos finales para calcular TMR
        # En este caso utilizaremos el valor de fin de cada proceso que esta en la tabla
        tmr_formula = "TMR=(" + "+".join(
            str(p.tiempo_retorno) for p in self.gestor_procesos.procesos) + f")/{n}={tmr:.2f} ut"
        # Mostrar los resultados con las fórmulas en una ventana emergente
        self.resultado_ventana = messagebox.showinfo("Resultados",
                                                     f"{secuencia_ejecucion}\n\n{tme_formula}\n{tmr_formula}")
        # Crear un frame para contener el mensaje con desplazamiento
        frame_mensaje = tk.Frame(self.ventana)
        frame_mensaje.pack(fill="both", expand=True)


        # Crear un scrollbar para desplazarse verticalmente
        scrollbar = ttk.Scrollbar(frame_mensaje, orient="vertical")
        scrollbar.pack(side="right", fill="y")

    def limpiar_tabla(self):
        for item in self.tabla.get_children():
            self.tabla.delete(item)

    def nueva_planificacion(self):
        self.limpiar_tabla()
        self.limpiar_campos()
        self.gestor_procesos.limpiar_procesos()
        self.canvas.delete("all")  # Limpiar la secuencia en el Canvas
        self.entrada_nombre.focus_set()


