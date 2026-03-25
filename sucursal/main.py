# Solo puedes importar las siguientes librerías y ninguna otra
from typing import List
from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.client import ServerProxy
from sys import argv
import os, json, math, threading, time


class Sucursal:
    def __init__(self, puerto_servel: str, nombre: str) -> None:
        self.nombre = nombre
        self.servel = ServerProxy(f"http://127.0.0.1:{puerto_servel}", allow_none=True)
        self.operativa = True
        self.lock = threading.Lock()
        self.config_votaciones = {}
        self.opciones_votaciones = {}
        self.habilitados = {}
        self.votos_locales = {}
        self.participantes = {}

    def solicitar_información(self) -> None:
        info = self.servel.solicitar_informacion()
        self.config_votaciones = info["temas_votaciones"]
        self.opciones_votaciones = info["opciones_votaciones"]
        self.habilitados = info["votantes_habilitados"]

    def cerrar_temporal(self) -> None:
        self.operativa = False

    def reanudar(self) -> None:
        self.operativa = True

    def reportar(self) -> None:
        with self.lock:
            if not self.operativa:
                return
            if self.votos_locales:
                self.servel.recibir_votos(self.nombre, self.votos_locales)
                self.votos_locales = {}
    def votar(
        self,
        id_votante: str,
        id_votacion: str,
        preferencias: List[str],
        estados: List[str],
    ) -> None:
        with self.lock:
            if not self.operativa:
                self.servel.publicar_evento(self.nombre, id_votante, "Cerrado", id_votacion)
                return

            if id_votacion not in self.config_votaciones:
                self.servel.publicar_evento(self.nombre, id_votante, "No existe", id_votacion)
                return

            es_corrupto = "Corrupto" in estados
            es_mov_reducida = "Mov. Reducida" in estados
            tiene_documentos = "Indocumentado" not in estados

            habilitados_votacion = self.habilitados.get(self.nombre, {}).get(id_votacion, [])
            inscrito_aqui = int(id_votante) in habilitados_votacion
            ya_voto = id_votante in self.participantes.get(id_votacion, set())

            if not tiene_documentos and not es_corrupto:
                self.servel.publicar_evento(self.nombre, id_votante, "Indocumentado", id_votacion)
                return

            if not inscrito_aqui and not es_mov_reducida:
                self.servel.publicar_evento(self.nombre, id_votante, "Sucursal incorrecta",
                                            id_votacion)
                return

            if ya_voto and not es_corrupto:
                self.servel.publicar_evento(self.nombre, id_votante, "Repetido", id_votacion)
                return

            self._procesar_voto(id_votante, id_votacion, preferencias, estados)

    def _procesar_voto(self, id_votante: str, id_votacion: str, preferencias: List[str],
                       estados: List[str]) -> None:
        opciones_validas_votacion = self.opciones_votaciones.get(id_votacion, [])
        voto_final = None
        if "Negacionista" in estados:
            opciones_candidatas = [opcion for opcion in opciones_validas_votacion
                                   if opcion not in preferencias]
        else:
            opciones_candidatas = [opcion for opcion in opciones_validas_votacion
                                   if opcion in preferencias]
        if len(opciones_candidatas) == 0:
            voto_final = "Blanco"
        elif len(opciones_candidatas) == 1:
            voto_final = opciones_candidatas[0]
        else:
            voto_final = "Nulo"
        if id_votacion not in self.votos_locales:
            self.votos_locales[id_votacion] = []
        self.votos_locales[id_votacion].append(voto_final)
        if id_votacion not in self.participantes:
            self.participantes[id_votacion] = set()
        self.participantes[id_votacion].add(id_votante)

    # Puedes agregar métodos adicionales si lo consideras necesario


if __name__ == "__main__":
    if len(argv) != 4 or not argv[1].isdigit():
        texto = """
        El comando debe ser ejecutado con el siguiente formato:
        <COMANDO_PYTHON> main.py <PUERTO> <PUERTO_SERVEL> <NOMBRE>

        Donde:
         - <COMANDO_PYTHON> es el comando para ejecutar Python en tu sistema operativo.
         - <PUERTO> es el puerto en el que se ejecutará el servidor RPC.
         - <PUERTO_SERVEL> es el puerto en el que se encuentra el servidor Servel.
         - <NOMBRE> es el nombre de la sucursal.
        """
        print(texto)
        exit(1)

    PUERTO = int(argv[1])
    PUERTO_SERVEL = int(argv[2])
    NOMBRE = argv[3]

    # DEBES dejar IP_TAREA como "127.0.0.1"
    # porque como "localhost" es un poco más lenta la comunicación
    # para los que tienen sistema Windows
    # Link de interés: https://superuser.com/a/595324
    IP_TAREA = "127.0.0.1"

    sucursal = Sucursal(PUERTO_SERVEL, NOMBRE)
    with SimpleXMLRPCServer((IP_TAREA, PUERTO), allow_none=True) as server:
        server.register_instance(sucursal)
        print(f"Sucursal {NOMBRE} activa en puerto {PUERTO}...")
        server.serve_forever()
        