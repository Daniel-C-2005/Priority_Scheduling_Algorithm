class Proceso:
    def __init__(self, nombre, tiempo_llegada, rafagaCPU, prioridad):
        self.nombre = nombre
        self.tiempo_llegada = tiempo_llegada
        self.rafagaCPU = rafagaCPU
        self.prioridad = prioridad
        self.tiempo_espera = 0
        self.tiempo_retorno = 0

class GestorProcesos:
    def __init__(self):
        self.procesos = []

    def agregar_proceso(self, proceso):
        if any(p.nombre == proceso.nombre for p in self.procesos):
            raise ValueError(f"Ya existe un proceso con el nombre '{proceso.nombre}'.")
        if proceso.rafagaCPU <= 0 or proceso.tiempo_llegada < 0 or proceso.prioridad < 0:
            raise ValueError("Los tiempos y la prioridad deben ser positivos.")
        self.procesos.append(proceso)

    def planificar_por_prioridad(self):
        procesos_pendientes = self.procesos[:]
        tiempo_actual = 0
        resultado = []

        while procesos_pendientes:
            procesos_disponibles = [p for p in procesos_pendientes if p.tiempo_llegada <= tiempo_actual]

            if procesos_disponibles:
                procesos_disponibles.sort(key=lambda x: (x.prioridad, x.tiempo_llegada))
                proceso = procesos_disponibles[0]

                proceso.tiempo_espera = max(0, tiempo_actual - proceso.tiempo_llegada)
                #Tiempo de retorno (Su formula es el tiempo de finalizacion - tiempo de llegada)
                proceso.tiempo_retorno = proceso.rafagaCPU + proceso.tiempo_espera + proceso.tiempo_llegada
                tiempo_inicio = tiempo_actual  # Tiempo de inicio del proceso
                tiempo_final = tiempo_inicio + proceso.rafagaCPU  # Tiempo final del proceso

                # Añadir la información del tiempo de inicio y final al resultado
                resultado.append(
                    (proceso.nombre, proceso.rafagaCPU, proceso.tiempo_llegada, proceso.prioridad,
                     proceso.tiempo_espera, proceso.tiempo_retorno, tiempo_inicio, tiempo_final))

                tiempo_actual += proceso.rafagaCPU
                procesos_pendientes.remove(proceso)
            else:
                tiempo_actual = min(p.tiempo_llegada for p in procesos_pendientes)

        return resultado

    def calcular_promedios(self):
        # Calcular los tiempos medios de espera y retorno de forma acumulativa
        total_espera = sum(p.tiempo_espera for p in self.procesos)
        #Sumaremos todos los datos de la tabla en FIN
        total_retorno = sum(p.tiempo_retorno for p in self.procesos)


        # Cantidad de procesos
        n = len(self.procesos)

        # Tiempos medios
        tme = total_espera / n
        tmr = total_retorno /n

        # Devolver también las sumas parciales para construir las fórmulas
        return tme, tmr, total_espera, total_retorno

    def limpiar_procesos(self):
        self.procesos.clear()
