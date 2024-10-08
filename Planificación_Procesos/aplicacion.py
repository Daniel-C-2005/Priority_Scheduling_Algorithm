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
        self.ventana.title("Planificación de Procesos por Prioridad")
        self.ventana.geometry("700x600")
        self.ventana.configure(bg="#eaeaea")
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
        etiqueta = tk.Label(self.ventana, text=texto, bg="#eaeaea", font=('Helvetica', 12, 'bold'))
        etiqueta.pack(pady=5)

        entrada = tk.Entry(self.ventana, bg="#ffffff", font=('Helvetica', 12), bd=1, relief="solid")
        entrada.pack(pady=5)
        if validar:
            entrada.config(validate="key", validatecommand=(self.ventana.register(validar), '%P'))
        return entrada

    def validar_numeros(self, nuevo_texto):
        return nuevo_texto.isdigit() or nuevo_texto == ""

    def crear_botones(self):
        tk.Button(self.ventana, text="Agregar Proceso", command=self.agregar_proceso, bg="#4CAF50", fg="white",
                  font=('Helvetica', 12)).pack(pady=5)
        tk.Button(self.ventana, text="Ejecutar Planificación", command=self.ejecutar_planificacion, bg="#2196F3",
                  fg="white", font=('Helvetica', 12)).pack(pady=5)
        tk.Button(self.ventana, text="Nueva Planificación", command=self.nueva_planificacion, bg="#FF5722",
                  fg="white", font=('Helvetica', 12)).pack(pady=5)

    def crear_tabla(self):
        self.tabla = ttk.Treeview(self.ventana, columns=('Proceso', 'Ráfaga CPU', 'Prioridad', 'Tiempo Espera', 'Tiempo Retorno'),
                                  show='headings')
        self.tabla.heading('Proceso', text='Proceso')
        self.tabla.heading('Ráfaga CPU', text='Ráfaga CPU')
        self.tabla.heading('Prioridad', text='Prioridad')
        self.tabla.heading('Tiempo Espera', text='Tiempo Espera')
        self.tabla.heading('Tiempo Retorno', text='Tiempo Retorno')

        for col in self.tabla['columns']:
            self.tabla.column(col, anchor='center')
        self.tabla.pack(pady=10, fill=tk.BOTH, expand=True)

    def crear_barra_progreso(self):
        self.barra_progreso = ttk.Progressbar(self.ventana, mode='indeterminate')
        self.barra_progreso.pack(pady=10, fill=tk.X)

    def crear_canvas_secuencia(self):
        self.canvas = tk.Canvas(self.ventana, height=150, bg="white")  # Altura aumentada para mayor claridad
        self.canvas.pack(pady=20, fill=tk.X)

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
            tiempo_espera_ut = f"{proceso[4]} ut"
            tiempo_retorno_ut = f"{proceso[5]} ut"
            self.tabla.insert("", tk.END, values=(proceso[0], proceso[1], proceso[3], tiempo_espera_ut, tiempo_retorno_ut))

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
            self.canvas.create_text(inicio, y + height + 10, text=str(proceso[2]), font=('Helvetica', 10))  # Tiempo de inicio
            self.canvas.create_text(fin, y + height + 10, text=str(proceso[5]), font=('Helvetica', 10))  # Tiempo de retorno

            x_actual = fin + 20  # Mover el siguiente rectángulo a la derecha con más espacio

            secuencia_ejecucion += f"{proceso[0]} ({proceso[5]}) "

        tme, tmr = self.gestor_procesos.calcular_promedios()
        tme_str = f"TME = {tme:.2f} ut"
        tmr_str = f"TMR = {tmr:.2f} ut"
        self.resultado_ventana = messagebox.showinfo("Resultados", f"{secuencia_ejecucion}\n\n{tme_str}\n{tmr_str}")

    def limpiar_tabla(self):
        for item in self.tabla.get_children():
            self.tabla.delete(item)

    def nueva_planificacion(self):
        self.limpiar_tabla()
        self.limpiar_campos()
        self.gestor_procesos.limpiar_procesos()
        self.canvas.delete("all")  # Limpiar la secuencia en el Canvas
        self.entrada_nombre.focus_set()


# Iniciar la aplicación
if __name__ == "__main__":
    root = tk.Tk()
    app = Aplicacion(root)
    root.mainloop()
