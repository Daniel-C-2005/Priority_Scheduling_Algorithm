class Proceso:
    def __init__(self, nombre, tiempo_llegada, rafagaCPU, prioridad):
        self.nombre = nombre
        self.tiempo_llegada = tiempo_llegada
        self.rafagaCPU = rafagaCPU
        self.prioridad = prioridad
        self.tiempo_espera = 0
        self.tiempo_retorno = 0
        self.tiempo_finalizacion = 0


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
            # Seleccionar procesos que ya hayan llegado al tiempo actual
            procesos_disponibles = [p for p in procesos_pendientes if p.tiempo_llegada <= tiempo_actual]

            if procesos_disponibles:
                # Priorizar por prioridad y tiempo de llegada en caso de empate
                procesos_disponibles.sort(key=lambda x: (x.prioridad, x.tiempo_llegada))
                proceso = procesos_disponibles[0]

                # Calcular tiempos de espera y retorno
                proceso.tiempo_espera = max(0, tiempo_actual - proceso.tiempo_llegada)
                tiempo_inicio = tiempo_actual
                tiempo_final = tiempo_inicio + proceso.rafagaCPU

                # El tiempo de retorno es el tiempo de finalización menos el tiempo de llegada
                proceso.tiempo_retorno = proceso.rafagaCPU + proceso.tiempo_espera + proceso.tiempo_llegada
                proceso.tiempo_finalizacion = tiempo_final

                # Añadir los resultados del proceso actual
                resultado.append(
                    (proceso.nombre, proceso.rafagaCPU, proceso.tiempo_llegada, proceso.prioridad,
                     proceso.tiempo_espera, proceso.tiempo_retorno, tiempo_inicio, tiempo_final)
                )

                # Avanzar el tiempo actual y remover el proceso de la lista pendiente
                tiempo_actual += proceso.rafagaCPU
                procesos_pendientes.remove(proceso)
            else:
                # Si no hay procesos disponibles, avanzar el tiempo al siguiente proceso en la lista
                tiempo_actual = min(p.tiempo_llegada for p in procesos_pendientes)

        return resultado

    def calcular_promedios(self):
        # Sumar los tiempos de espera y retorno de todos los procesos
        total_espera = sum(p.tiempo_espera for p in self.procesos)
        total_retorno = sum(p.tiempo_retorno for p in self.procesos)

        # Cantidad de procesos
        n = len(self.procesos)

        if n == 0:
            raise ValueError("No hay procesos para calcular promedios.")

        # Calcular TME (Tiempo Medio de Espera) y TMR (Tiempo Medio de Retorno)
        tme = total_espera / n
        tmr = total_retorno / n

        # Crear los detalles de cálculo para cada proceso
        detalles = [
            {
                'nombre': p.nombre,
                'tiempo_espera': p.tiempo_espera,
                'tiempo_retorno': p.tiempo_retorno
            }
            for p in self.procesos
        ]

        return tme, tmr, detalles

    def limpiar_procesos(self):
        self.procesos.clear()

