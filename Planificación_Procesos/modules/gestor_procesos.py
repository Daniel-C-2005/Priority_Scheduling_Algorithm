# gestor_procesos.py
class Proceso:
    def __init__(self, nombre, tiempo_llegada, tiempo_ejecucion, prioridad):
        self.nombre = nombre
        self.tiempo_llegada = tiempo_llegada
        self.tiempo_ejecucion = tiempo_ejecucion
        self.prioridad = prioridad
        self.tiempo_espera = 0
        self.tiempo_retorno = 0

class GestorProcesos:
    def __init__(self):
        self.procesos = []

    def agregar_proceso(self, proceso):
        if any(p.nombre == proceso.nombre for p in self.procesos):
            raise ValueError(f"Ya existe un proceso con el nombre '{proceso.nombre}'.")
        if proceso.tiempo_ejecucion <= 0 or proceso.tiempo_llegada < 0 or proceso.prioridad < 0:
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

                proceso.tiempo_espera = tiempo_actual - proceso.tiempo_llegada
                proceso.tiempo_retorno = proceso.tiempo_espera + proceso.tiempo_ejecucion

                resultado.append(
                    (proceso.nombre, proceso.tiempo_ejecucion, proceso.tiempo_llegada, proceso.prioridad,
                     proceso.tiempo_espera, proceso.tiempo_retorno))

                tiempo_actual += proceso.tiempo_ejecucion
                procesos_pendientes.remove(proceso)
            else:
                tiempo_actual = min(p.tiempo_llegada for p in procesos_pendientes)

        return resultado

    def calcular_promedios(self):
        total_espera = sum(p.tiempo_espera for p in self.procesos)
        total_retorno = sum(p.tiempo_retorno for p in self.procesos)

        tme = total_espera / len(self.procesos)
        tmr = total_retorno / len(self.procesos)

        return tme, tmr

    def limpiar_procesos(self):
        self.procesos.clear()
