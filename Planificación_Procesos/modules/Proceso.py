class Proceso:
    def __init__(self, nombre, tiempo_llegada, rafagaCPU, prioridad):
        self.nombre = nombre  # Nombre del proceso
        self.tiempo_llegada = tiempo_llegada  # Tiempo de llegada del proceso
        self.rafagaCPU = rafagaCPU  # Ráfaga de CPU o duración de ejecución
        self.prioridad = prioridad  # Prioridad del proceso
        self.tiempo_espera = 0  # Tiempo de espera inicializado en 0
        self.tiempo_retorno = 0  # Tiempo de retorno inicializado en 0
