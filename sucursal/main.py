# Solo puedes importar las siguientes librerías y ninguna otra
from typing import List
from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.client import ServerProxy
from sys import argv
import os, json, math, threading, time


class Sucursal:
    def __init__(self, puerto_servel: str, nombre: str) -> None:
        pass

    def solicitar_información(self) -> None:
        pass

    def cerrar_temporal(self) -> None:
        pass

    def reanudar(self) -> None:
        pass

    def reportar(self) -> None:
        pass

    def votar(
        self,
        id_votante: str,
        id_votacion: str,
        preferencias: List[str],
        estados: List[str],
    ) -> None:
        pass

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
    # Completar con lo que falta
