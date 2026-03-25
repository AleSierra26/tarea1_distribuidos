# Solo puedes importar las siguientes librerías y ninguna otra
from xmlrpc.server import SimpleXMLRPCServer
from sys import argv
import os, json, math, threading, time


class Servel:
    def __init__(self, archivo_configuracion: str, archivo_log: str) -> None:
        ruta_config = os.path.join("votes_configurations", f"{archivo_configuracion}.json")
        with open(ruta_config, "r", encoding="utf-8") as archivo:
            self.config = json.load(archivo)
        self.archivo_log = archivo_log
        self.ruta_log = os.path.join("logs", f"{archivo_log}.txt")
        with open(self.ruta_log, "w", encoding="utf-8") as archivo:
            pass
        self.votos_globales = {}
        self.lock = threading.Lock()
        self.nombres_votantes = {}
        self.ruta_subscriptores = "subscriptors"
        self.suscriptores = {}
        with open("votantes.csv", "r", encoding="utf-8") as archivo:
            next(archivo)
            for linea in archivo:
                user_id, nombre = linea.strip().split(",", 1)
                self.nombres_votantes[user_id] = nombre

    def recibir_votos(self, sucursal: str, votos: dict) -> None:
        total_recibidos = 0
        with self.lock:
            for id_voto, lista in votos.items():
                if id_voto not in self.votos_globales:
                    self.votos_globales[id_voto] = {}
                for voto in lista:
                    self.votos_globales[id_voto][voto] = (self.votos_globales[id_voto].get(voto, 0)
                                                          + 1)
                    total_recibidos += 1
            with open(self.ruta_log, "a", encoding="utf-8") as archivo:
                archivo.write(f"Sucursal {sucursal} ha enviado información: {total_recibidos}\n")

    def ganador(self, id_votacion: str) -> None:
        with self.lock:
            tema = self.config["temas_votaciones"].get(id_votacion, "Desconocido")
            votos_votacion = self.votos_globales.get(id_votacion, {})
            opciones_validas = self.config["opciones_votaciones"].get(id_votacion, [])
            conteos = {opcion: votos_votacion.get(opcion, 0) for opcion in opciones_validas}
            total_votos_validos = sum(conteos.values())
            with open(self.ruta_log, "a", encoding="utf-8") as archivo:
                if total_votos_validos == 0:
                    archivo.write(f"Ganador {tema}: No se puede determinar\n")
                else:
                    max_votos = max(conteos.values())
                    ganadores = [opcion for opcion, voto in conteos.items() if voto == max_votos]
                    if len(ganadores) > 1:
                        archivo.write(f"Ganador {tema}: Empate\n")
                    else:
                        archivo.write(f"Ganador {tema}: {ganadores[0]}\n")

    def log(self, id_votacion: str, opcion: str) -> None:
        with self.lock:
            tema = self.config["temas_votaciones"].get(id_votacion, "Desconocido")
            opciones_permitidas = self.config["opciones_votaciones"].get(id_votacion, [])
            es_opcion_valida = opcion in opciones_permitidas or opcion in ["Nulo", "Blanco"]
            with open(self.ruta_log, "a", encoding="utf-8") as archivo:
                if es_opcion_valida:
                    cantidad = self.votos_globales.get(id_votacion, {}).get(opcion, 0)
                    archivo.write(f"Votos {tema} ({opcion}): {cantidad}\n")
                else:
                    archivo.write(f"Votos {tema} ({opcion}): No existe\n")

    def new_subscriber(self, subscriptor: str) -> None:
        with self.lock:
            ruta_archivo = os.path.join(self.ruta_subscriptores, subscriptor)
            if os.path.exists(ruta_archivo):
                os.remove(ruta_archivo)
            with open(ruta_archivo, "w", encoding="utf-8") as archivo:
                pass
            self.suscriptores[subscriptor] = set()

    def subscribe(self, subscriptor: str, sucursal: str, evento: str) -> None:
        with self.lock:
            if subscriptor not in self.suscriptores:
                return
            nuevo_filtro = (sucursal, evento)
            self.suscriptores[subscriptor].add(nuevo_filtro)

    def unsubscribe(self, subscriptor: str, sucursal: str, evento: str) -> None:
        with self.lock:
            if subscriptor in self.suscriptores:
                filtro = (sucursal, evento)
                if filtro in self.suscriptores[subscriptor]:
                    self.suscriptores[subscriptor].remove(filtro)
                    
    def publicar_evento(self, sucursal: str, id_votante: str, evento: str,
                        id_votacion: str) -> None:
        with self.lock:
            nombre_completo = self.nombres_votantes.get(str(id_votante), "Desconocido")
            tema_o_id = self.config["temas_votaciones"].get(id_votacion, id_votacion)
            linea_notificacion = f"{sucursal};{tema_o_id};{evento};{nombre_completo}\n"
            for subscriptor, filtros in self.suscriptores.items():
                notificar = False
                for filtro_sucursal, filtro_evento in filtros:
                    match_sucursal = (filtro_sucursal == "*" or filtro_sucursal == sucursal)
                    match_evento = (filtro_evento == "*" or filtro_evento == evento)
                    if match_sucursal and match_evento:
                        notificar = True
                        break
                if notificar:
                    ruta_archivo = os.path.join(self.ruta_subscriptores, subscriptor)
                    with open(ruta_archivo, "a", encoding="utf-8") as archivo:
                        archivo.write(linea_notificacion)

    def solicitar_informacion(self) -> dict:
        return {
            "temas_votaciones": self.config["temas_votaciones"],
            "opciones_votaciones": self.config["opciones_votaciones"],
            "votantes_habilitados": self.config["votantes_habilitados_sucursal"]
        }

    # Puedes agregar métodos adicionales si lo consideras necesario


if __name__ == "__main__":
    if len(argv) != 4 or not argv[1].isdigit():
        texto = """
        El comando debe ser ejecutado con el siguiente formato:
        <COMANDO_PYTHON> main.py <PUERTO> <CONFIGURACION> <LOGS>

        Donde:
         - <COMANDO_PYTHON> es el comando para ejecutar Python en tu sistema operativo.
         - <PUERTO> es el puerto en el que se ejecutará el servidor RPC.
         - <CONFIGURACION> es el nombre de un archivo JSON con la configuración de la votación.
         - <LOGS> es el nombre de un archivo TXT donde se guardarán los logs de la votación.
        """
        print(texto)
        exit(1)

    PUERTO = int(argv[1])
    CONFIGURACION = argv[2]
    LOGS = argv[3]

    # DEBES dejar IP_TAREA como "127.0.0.1"
    # porque como "localhost" es un poco más lenta la comunicación
    # para los que tienen sistema Windows
    # Link de interés: https://superuser.com/a/595324
    IP_TAREA = "127.0.0.1"

    servel_votaciones = Servel(CONFIGURACION, LOGS)
    with SimpleXMLRPCServer((IP_TAREA, PUERTO), allow_none=True) as server:
        server.register_instance(servel_votaciones)
        print(f"Servidor Servel funcionando en el puerto {PUERTO}...")
        server.serve_forever()
